import pytest
from flask_jwt_extended import create_access_token

from labconnect import db
from labconnect.models import ManagementPermissions, User


@pytest.fixture
def setup_database(test_client):
    """Set up and tear down database for each test"""
    # rollback database for upcoming test
    db.session.rollback()
    db.session.remove()
    
    # Clean up existing data
    db.session.execute(db.text("TRUNCATE TABLE management_permissions CASCADE"))
    db.session.execute(db.text("TRUNCATE TABLE \"user\" CASCADE"))
    db.session.commit()

    yield


@pytest.fixture
def setup_users(test_client, setup_database):
    """Set up test users and permissions"""
    # add super admin user
    super_admin = User(
        id="superadm1",
        email="superadmin@example.com",
        first_name="Super",
        last_name="Admin"
    )
    db.session.add(super_admin)
    db.session.commit()
    
    super_admin_perms = ManagementPermissions(
        user_id=super_admin.id,
        super_admin=True,
        admin=False
    )
    db.session.add(super_admin_perms)
    
    # add promotable user
    regular_user = User(
        id="regular01",
        email="regular@example.com",
        first_name="Regular",
        last_name="User"
    )
    db.session.add(regular_user)
    db.session.commit()
    
    regular_user_perms = ManagementPermissions(
        user_id=regular_user.id,
        super_admin=False,
        admin=False
    )
    db.session.add(regular_user_perms)

    # add demotable user
    regular_user2 = User(
        id="regular02",
        email="regular2@example.com",
        first_name="Regular2",
        last_name="User2"
    )
    db.session.add(regular_user2)
    db.session.commit()
    
    regular_user2_perms = ManagementPermissions(
        user_id=regular_user2.id,
        super_admin=False,
        admin=True
    )
    db.session.add(regular_user2_perms)
    
    # add non-super-admin user
    non_admin = User(
        id="nonadmin1",
        email="nonadmin@example.com",
        first_name="Non",
        last_name="Admin"
    )
    db.session.add(non_admin)
    db.session.commit()
    
    non_admin_perms = ManagementPermissions(
        user_id=non_admin.id,
        super_admin=False,
        admin=True
    )
    db.session.add(non_admin_perms)
    
    db.session.commit()
    
    yield {
        "super_admin": super_admin,
        "regular_user": regular_user,
        "regular_user2": regular_user2,
        "non_admin": non_admin
    }


@pytest.fixture
def create_access_token_for_user(test_client):
    """Create a real JWT access token for testing"""
    
    def _create_token(user_id):
        return create_access_token(identity=user_id)
    
    return _create_token


def test_promote_user_success(test_client, setup_users, create_access_token_for_user):
    """Test successful user promotion by super admin"""
    users = setup_users
    access_token = create_access_token_for_user(users["super_admin"].id)
    
    # make the request with url to ensure cookies work
    response = test_client.patch(
        f"/users/{users['regular_user'].email}/permissions",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"change_status": True},
    )
    
    assert response.status_code == 200
    assert response.json["msg"] == "User Lab Manager permissions changed!"
    
    # verify the user was actually promoted
    promoted_perms = db.session.query(ManagementPermissions).filter_by(
        user_id=users["regular_user"].id
    ).first()
    assert promoted_perms.admin is True

def test_demote_user_success(test_client, setup_users, create_access_token_for_user):
    """Test successful user demotion by super admin"""
    users = setup_users
    access_token = create_access_token_for_user(users["super_admin"].id)
    
    # demote user
    response = test_client.patch(
        f"/users/{users['regular_user2'].email}/permissions",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"change_status": True},
    )
    
    assert response.status_code == 200
    assert response.json["msg"] == "User Lab Manager permissions changed!"
    
    # verify the user was actually promoted
    demoted_perms = db.session.query(ManagementPermissions).filter_by(
        user_id=users["regular_user2"].id
    ).first()
    assert demoted_perms.admin is False

def test_promote_user_no_json_data(test_client, setup_users, 
                                   create_access_token_for_user):
    """Test promotion fails when no JSON data is provided"""
    users = setup_users
    access_token = create_access_token_for_user(users["super_admin"].id)
    
    response = test_client.patch(
        f"/users/{users['regular_user'].email}/permissions",
        headers={"Authorization": f"Bearer {access_token}"},
        content_type='application/json'
    )
    
    assert response.status_code == 400


def test_promote_user_no_super_admin_perms(test_client, setup_users, 
                                           create_access_token_for_user):
    """Test promotion fails when promoter is not a super admin"""
    users = setup_users
    access_token = create_access_token_for_user(users["non_admin"].id)
    
    
    
    response = test_client.patch(
        f"/users/{users['regular_user'].email}/permissions",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"change_status": True}
    )
    
    assert response.status_code == 401
    assert response.json["msg"] == "Missing permissions"


def test_promote_user_promoter_has_no_perms_record(test_client, setup_users, 
                                                   create_access_token_for_user):
    """Test promotion fails when promoter has no permissions record"""
    users = setup_users
    
    # add user with no perms
    user_no_perms = User(
        id="noperms01",
        email="noperms@example.com",
        first_name="No",
        last_name="Perms"
    )
    db.session.add(user_no_perms)
    db.session.commit()
    
    access_token = create_access_token_for_user(user_no_perms.id)
    
    response = test_client.patch(
        f"/users/{users['regular_user'].email}/permissions",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"change_status": True}
    )
    
    assert response.status_code == 401
    assert response.json["msg"] == "Missing permissions"


def test_promote_user_target_not_found(test_client, setup_users, 
                                       create_access_token_for_user):
    """Test promotion fails when target user doesn't exist"""
    users = setup_users
    access_token = create_access_token_for_user(users["super_admin"].id)
    
    response = test_client.patch(
        "/users/nonexistent@example.com/permissions",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"change_status": True}
    )
    
    assert response.status_code == 500
    assert response.json["msg"] == "No user matches RCS ID"


def test_promote_user_no_jwt_token(test_client, setup_users):
    """Test promotion fails when no JWT token is provided"""
    users = setup_users
    
    # clear existing cookies
    test_client.delete_cookie('access_token')
    
    response = test_client.patch(
        f"/users/{users['regular_user'].email}/permissions",
        json={"change_status": True}
    )
    
    assert response.status_code == 401