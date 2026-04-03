import pytest
from app import app

@pytest.fixture
def client():
app.config['TESTING'] = True
with app.test_client() as client:
yield client

# Test Home Page

def test_home(client):
response = client.get("/")
assert response.status_code == 200

# Test Add API

def test_add(client):
response = client.get("/add?a=5&b=3")
assert response.status_code == 200
assert response.get_json()["result"] == 8

# Test Subtract API

def test_subtract(client):
response = client.get("/sub?a=10&b=4")
assert response.status_code == 200
assert response.get_json()["result"] == 6

# Test Multiply API

def test_multiply(client):
response = client.get("/mul?a=6&b=2")
assert response.status_code == 200
assert response.get_json()["result"] == 12

# Test Divide API

def test_divide(client):
response = client.get("/div?a=10&b=2")
assert response.status_code == 200
assert response.get_json()["result"] == 5

# Test Division by Zero

def test_divide_by_zero(client):
response = client.get("/div?a=10&b=0")
assert response.status_code == 400
assert "error" in response.get_json()

# Test Invalid Input

def test_invalid_input(client):
response = client.get("/add?a=x&b=2")
assert response.status_code == 400

# Test Metrics Endpoint (Prometheus)

def test_metrics(client):
response = client.get("/metrics")
assert response.status_code == 200
assert b"app_requests_total" in response.data

