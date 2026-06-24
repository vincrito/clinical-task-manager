"""
Shared pytest fixtures for the personal-task-manager test suite.
"""
import pytest
from app import create_app
from models import db as _db

_TEST_CONFIG = {
    "TESTING": True,
    "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    "WTF_CSRF_ENABLED": False,
    "SECRET_KEY": "test-secret",
}


@pytest.fixture(scope="session")
def app():
    """Create a Flask application configured for testing with an in-memory DB."""
    application = create_app(test_config=_TEST_CONFIG)
    with application.app_context():
        _db.create_all()
        yield application
        _db.drop_all()


@pytest.fixture
def db(app):
    """Yield the DB inside an app context; roll back after each test."""
    with app.app_context():
        yield _db
        _db.session.rollback()


@pytest.fixture
def client(app):
    """Provide a test client."""
    return app.test_client()


@pytest.fixture
def user(db):
    """Create and return a test user."""
    from models.user import User, bcrypt
    u = User(
        username="testuser",
        password_hash=bcrypt.generate_password_hash("password").decode("utf-8"),
    )
    db.session.add(u)
    db.session.commit()
    yield u
    # Clean up all tasks/lists/rules tied to this user, then the user itself
    from models.task import Task
    from models.list import TaskList
    from models.recurrence import RecurrenceRule
    Task.query.filter_by(user_id=u.id).delete(synchronize_session=False)
    RecurrenceRule.query.filter_by(user_id=u.id).delete(synchronize_session=False)
    TaskList.query.filter_by(user_id=u.id).delete(synchronize_session=False)
    db.session.delete(u)
    db.session.commit()


@pytest.fixture
def task_list(db, user):
    """Create and return a TaskList for the test user."""
    from models.list import TaskList
    lst = TaskList(user_id=user.id, name="Test List")
    db.session.add(lst)
    db.session.commit()
    yield lst
    # Cleanup handled by user fixture teardown
