import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.db import get_db
from app.main import app

client = TestClient(app)

FARMER_OK = {
    "nome": "Manuel Bemba",
    "provincia": "Huíla",
    "cultura": "milho",
    "latitude": -14.9,
    "longitude": 13.5,
}


@pytest.fixture(autouse=True)
def db_temporaria():
    """BD SQLite em memória, nova para cada teste."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    def get_test_db():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db
    yield
    app.dependency_overrides.clear()


def test_post_valido_devolve_201():
    response = client.post("/farmers", json=FARMER_OK)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["nome"] == "Manuel Bemba"
    assert data["provincia"] == "Huíla"


def test_get_por_id_e_404_se_inexistente():
    criado = client.post("/farmers", json=FARMER_OK).json()

    encontrado = client.get(f"/farmers/{criado['id']}")
    assert encontrado.status_code == 200
    assert encontrado.json() == criado

    inexistente = client.get("/farmers/999")
    assert inexistente.status_code == 404


def test_post_invalido_devolve_422():
    invalido = {**FARMER_OK, "latitude": 10}  # fora de -18 a -4

    response = client.post("/farmers", json=invalido)

    assert response.status_code == 422