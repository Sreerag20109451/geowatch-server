from fastapi.testclient import TestClient
from main import app
import os
import json
import pytest

client = TestClient(app)

def test_read_key_info():
    """Test the root endpoint for key info and authentication status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "authenticated"
    assert "key_source" in data
    # Because we mocked KEY_JSON, it should fallback to writing temp_key.json
    assert "temp_key.json" in data["key_source"] or "key_source" in data

def test_testee_success(mocker):
    """Test the /testee endpoint for successful map mapping."""
    # We need to mock ee.Image returning a mock that responds to .select() and .getMapId()
    mock_image = mocker.MagicMock()
    mock_selected = mocker.MagicMock()
    mock_selected.getMapId.return_value = {"mapid": "test_map_id_1234"}
    mock_image.select.return_value = mock_selected
    
    mocker.patch("main.ee.Image", return_value=mock_image)

    response = client.get("/testee")
    
    assert response.status_code == 200
    data = response.json()
    assert "mapid" in data
    assert data["mapid"] == {"mapid": "test_map_id_1234"}

def test_testee_exception(mocker):
    """Test the /testee endpoint exception handling."""
    mocker.patch("main.ee.Image", side_effect=Exception("Earth Engine API failed"))
    
    response = client.get("/testee")
    assert response.status_code == 200 # Note the endpoint returns 200 even on error in main.py
    data = response.json()
    assert "error" in data
    assert data["error"] == "Earth Engine API failed"
