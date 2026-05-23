import os

import pytest
from flask_jwt_extended import create_access_token
from sqlalchemy import Text, event

# Use SQLite for local pytest unless CI/dev sets a Postgres DB URL.
os.environ.setdefault("DB", "sqlite:///:memory:")

from labconnect import create_app, db
from labconnect.models import Opportunities, User, update_search_vector

from tests.seed import seed_development_data


def _use_sqlite() -> bool:
    uri = os.environ.get("DB", "")
    return uri.startswith("sqlite")


def _configure_sqlite_models() -> None:
    if Opportunities.__table__ is not None:
        Opportunities.__table__.c.search_vector.type = Text()
    Opportunities.__table_args__ = ()
    for listener in (update_search_vector,):
        for hook in ("before_insert", "before_update"):
            try:
                event.remove(Opportunities, hook, listener)
            except Exception:
                pass


if _use_sqlite():
    _configure_sqlite_models()


requires_postgres = pytest.mark.skipif(
    _use_sqlite(), reason="This test requires PostgreSQL-specific SQL"
)


@pytest.fixture(scope="session")
def test_client():
    flask_app = create_app()
    flask_app.config.update(
        {
            "TESTING": True,
            "DEBUG": True,
            "SQLALCHEMY_DATABASE_URI": os.environ["DB"],
            "JWT_TOKEN_LOCATION": ["headers"],
            "JWT_COOKIE_CSRF_PROTECT": False,
            "JWT_COOKIE_SECURE": False,
        }
    )

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.drop_all()
            db.create_all()
            seed_development_data()
        yield testing_client
        with flask_app.app_context():
            db.session.remove()
            db.engine.dispose()


@pytest.fixture
def auth_headers(test_client):
    """Bearer token for a seeded or custom user."""

    def _headers(email: str = "test@rpi.edu"):
        with test_client.application.app_context():
            token = create_access_token(identity=email)
        return {"Authorization": f"Bearer {token}"}

    return _headers


@pytest.fixture
def login_as_test_user(test_client, auth_headers):
    """Authorization headers for test@rpi.edu via the dev login shortcut."""

    response = test_client.get("/login")
    assert response.status_code == 302
    redirect_url = response.headers["Location"]
    code = redirect_url.split("code=")[1].split("&")[0]

    token_response = test_client.post("/token", json={"code": code})
    assert token_response.status_code == 200

    return auth_headers("test@rpi.edu")
