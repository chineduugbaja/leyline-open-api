import pytest
import json
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
    response = client.get('/v1/tools/lookup?domain=google.com')
    assert response.status_code == 200
    assert 'addresses' in response.json

def test_history_endpoint(client):
    """Test the /v1/history endpoint"""
    response = client.get('/v1/history')
    assert response.status_code == 200
    data = json.loads(response.data)
    # Add more specific checks based on your actual data structure
    assert isinstance(data, list)  # Example check to ensure it's a list
    assert len(data) > 0  # Ensure there is at least one record for the test

def test_validate_ip_endpoint(client):
    """Test the /v1/tools/validate endpoint"""
    valid_ip = {'ip': '192.168.1.1'}
    response = client.post('/v1/tools/validate', json=valid_ip)
    assert response.status_code == 200
    assert json.loads(response.data) == {"status": True}

    invalid_ip = {'ip': '999.999.999.999'}
    response = client.post('/v1/tools/validate', json=invalid_ip)
    assert response.status_code == 400
    assert json.loads(response.data) == {"status": False}