import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_add(client):
    response = client.get("/add?a=5&b=3")
    assert response.status_code == 200
    assert response.get_json()["result"] == 8


def test_subtract(client):
    response = client.get("/sub?a=10&b=4")
    assert response.status_code == 200
    assert response.get_json()["result"] == 6


def test_multiply(client):
    response = client.get("/mul?a=6&b=2")
    assert response.status_code == 200
    assert response.get_json()["result"] == 12


def test_divide(client):
    response = client.get("/div?a=10&b=2")
    assert response.status_code == 200
    assert response.get_json()["result"] == 5


def test_divide_by_zero(client):
    response = client.get("/div?a=10&b=0")
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_invalid_input(client):
    response = client.get("/add?a=x&b=2")
    assert response.status_code == 400

def test_divide_invalid_input(client):
    response = client.get("/div?a=x&b=2")
    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid input"

def test_subtract_invalid_input(client):
    response = client.get("/sub?a=x&b=2")
    assert response.status_code == 400

def test_multiply_invalid_input(client):
    response = client.get("/mul?a=x&b=2")
    assert response.status_code == 400


def test_metrics(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"app_requests_total" in response.data
