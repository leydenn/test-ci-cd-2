import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, get_db
from sqlalchemy.orm import Session

client = TestClient(app)

# Создаём тестовую БД
@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from FastAPI!"}

def test_create_message():
    response = client.post("/messages", json={
        "username": "testuser",
        "content": "Hello, world!"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["content"] == "Hello, world!"
    assert "id" in data
    assert "created_at" in data

def test_get_messages():
    # Сначала создадим сообщение
    client.post("/messages", json={
        "username": "user1",
        "content": "Test message"
    })
    
    # Потом получим список
    response = client.get("/messages")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["content"] == "Test message"

def test_empty_messages():
    # Очищаем БД (фикстура сделает это автоматически)
    response = client.get("/messages")
    assert response.status_code == 200
    # В новой БД сообщений нет
    assert len(response.json()) == 0