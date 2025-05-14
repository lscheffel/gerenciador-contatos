import pytest
import sys
from sqlalchemy.sql import text
print("sys.path:", sys.path)  # Debug
from app import create_app
from app.models import Contact, init_db
from app.database import SessionLocal, engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def setup_database():
    init_db()
    yield
    engine.dispose()  # Fecha todas as conexões do engine
    print("Teardown setup_database concluído, engine liberado")  # Debug

@pytest.fixture
def client(setup_database):
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def db(setup_database):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    yield db
    db.query(Contact).delete()
    db.commit()
    db.close()
    print("Teardown db concluído")  # Debug

def test_create_contact(client, db):
    print("Executando test_create_contact")  # Debug
    response = client.post(
        "/api/contacts",  # Corrigido de "contatos" para "contacts"
        json={"name": "João", "email": "joao@email.com", "phone": "123456789"},
    )
    print(f"Resposta: {response.status_code}, {response.get_json()}")  # Debug
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "João"
    assert data["email"] == "joao@email.com"

def test_get_contacts(client, db):
    print("Executando test_get_contacts")  # Debug
    db.add(Contact(name="João", email="joao@email.com", phone="123456789"))
    db.commit()
    response = client.get("/api/contacts")
    print(f"Resposta: {response.status_code}, {response.get_json()}")  # Debug
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "João"