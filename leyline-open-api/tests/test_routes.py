import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """Test the /health endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'status': 'healthy'}

def test_root_endpoint(client):
    """Test the root endpoint /"""
    response = client.get('/')
    assert response.status_code == 200
    assert 'version' in response.json
    assert 'date' in response.json
    assert 'kubernetes' in response.json

def test_lookup_domain(client):
    """Test the /v1/tools/lookup endpoint"""
    response = client.get('/v1/tools/lookup?domain=example.com')
    assert response.status_code == 200
    assert 'addresses' in response.json
