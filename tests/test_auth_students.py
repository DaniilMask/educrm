from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.dependencies import get_db
from app.main import app
from app.models.user import User
from app.security import hash_password


TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def setup_module():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db


def teardown_module():
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def _create_user(phone: str = "79990000001", password: str = "secret123"):
    db = TestingSessionLocal()
    db_user = User(
        full_name="Test User",
        role="admin",
        phone=phone,
        password_hash=hash_password(password),
    )
    db.add(db_user)
    db.commit()
    db.close()


def _get_token(client: TestClient, phone: str, password: str) -> str:
    response = client.post(
        "/login",
        json={"phone": phone, "password": password},
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    return body["access_token"]


def test_login_invalid_credentials():
    client = TestClient(app)

    response = client.post(
        "/login",
        json={"phone": "70000000000", "password": "wrong"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_protected_students_crud_flow():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    _create_user()

    client = TestClient(app)
    token = _get_token(client, "79990000001", "secret123")
    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/students/",
        json={"full_name": "Ivan Ivanov", "phone": "78880000000"},
        headers=headers,
    )
    assert create_response.status_code == 200
    student_id = create_response.json()["id"]

    list_response = client.get("/students/", headers=headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    update_response = client.put(
        f"/students/{student_id}",
        json={"status": "inactive"},
        headers=headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "inactive"

    delete_response = client.delete(f"/students/{student_id}", headers=headers)
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Student deleted"


def test_students_requires_auth():
    client = TestClient(app)
    response = client.get("/students/")
    assert response.status_code == 401
