import pytest
from flask import Flask
from labconnect.models import User, ManagementPermissions
from labconnect import db
from flask_jwt_extended import create_access_token



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
        "non_admin": non_admin
    }


@pytest.fixture
def create_access_token_for_user():
    """Create a real JWT access token for testing"""
    
    def _create_token(user_id):
        return create_access_token(identity=user_id)
    
    return _create_token


def test_promote_user_success(test_client, setup_users, create_access_token_for_user):
    """Test successful user promotion by super admin"""
    users = setup_users
    access_token = create_access_token_for_user(users["super_admin"].id)
    
    # set the JWT token as a cookie
    test_client.set_cookie('access_token', access_token)
    
    response = test_client.patch(
        f"/users/{users['regular_user'].email}/permissions",
        json={"promote": True}
    )
    
    assert response.status_code == 200
    assert response.json["msg"] == "User promoted to Lab Manager"
    
    # verify the user was actually promoted
    promoted_perms = db.session.query(ManagementPermissions).filter_by(
        user_id=users["regular_user"].id
    ).first()
    assert promoted_perms.admin is True


def test_promote_user_no_json_data(test_client, setup_users, create_access_token_for_user):
    """Test promotion fails when no JSON data is provided"""
    users = setup_users
    access_token = create_access_token_for_user(users["super_admin"].id)
    
    # set the JWT token as a cookie
    test_client.set_cookie('access_token', access_token)
    
    response = test_client.patch(
        f"/users/{users['regular_user'].email}/permissions",
        content_type='application/json'
    )
    
    assert response.status_code == 400


def test_promote_user_no_super_admin_perms(test_client, setup_users, create_access_token_for_user):
    """Test promotion fails when promoter is not a super admin"""
    users = setup_users
    access_token = create_access_token_for_user(users["non_admin"].id)
    
    # set the JWT token as a cookie
    test_client.set_cookie('access_token', access_token)
    
    response = test_client.patch(
        f"/users/{users['regular_user'].email}/permissions",
        json={"promote": True}
    )
    
    assert response.status_code == 401
    assert response.json["msg"] == "Missing permissions"


def test_promote_user_promoter_has_no_perms_record(test_client, setup_users, create_access_token_for_user):
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
    
    # set the JWT token as a cookie
    test_client.set_cookie('access_token', access_token)
    
    response = test_client.patch(
        f"/users/{users['regular_user'].email}/permissions",
        json={"promote": True}
    )
    
    assert response.status_code == 401
    assert response.json["msg"] == "Missing permissions"


def test_promote_user_target_not_found(test_client, setup_users, create_access_token_for_user):
    """Test promotion fails when target user doesn't exist"""
    users = setup_users
    access_token = create_access_token_for_user(users["super_admin"].id)
    
    # set the JWT token as a cookie
    test_client.set_cookie('access_token', access_token)
    
    response = test_client.patch(
        "/users/nonexistent@example.com/permissions",
        json={"promote": True}
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
        json={"promote": True}
    )
    
    assert response.status_code == 401