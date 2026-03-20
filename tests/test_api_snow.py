import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_snow_cover_modis_success(mocker):
    """Test Modis snow cover successful response."""
    # Mock ModisProducts.get_modis_snow_cover
    mock_get_modis_snow_cover = mocker.patch("api.snow.modisproducts.get_modis_snow_cover")
    mock_get_modis_snow_cover.return_value = {
        "image": "mocked_modis_image",
        "vis_param": {"mock": "vis"},
        "legend": {"mock": "legend"}
    }
    
    # Mock EarthEngineMaps.get_mapid
    mock_get_mapid = mocker.patch("api.snow.maps.get_mapid")
    mock_get_mapid.return_value = {"url": "https://mocked.url/mapid"}
    
    response = client.get("/apiv0/snow/global_snow_cover?dataset=modis&region=TestRegion")
    assert response.status_code == 200
    data = response.json()
    assert data["url"] == "https://mocked.url/mapid"
    assert data["vis_params"] == {"mock": "vis"}
    assert data["legend"] == {"mock": "legend"}
    assert data["resolution"] == "mid"

def test_snow_cover_modis_exception(mocker):
    """Test exception handling for Modis."""
    mock_get_modis_snow_cover = mocker.patch("api.snow.modisproducts.get_modis_snow_cover")
    mock_get_modis_snow_cover.side_effect = Exception("Modis API failed")
    
    response = client.get("/apiv0/snow/global_snow_cover?dataset=modis")
    assert response.status_code == 500
    assert response.json() == {"error": "Modis API failed"}

def test_snow_cover_sentinel_success(mocker):
    """Test Sentinel snow cover successful response."""
    # Mock SentinelProducts.get_sentinel_snow_cover_composite
    mock_get_sentinel_snow_cover = mocker.patch("api.snow.sentinelproducts.get_sentinel_snow_cover_composite")
    mock_get_sentinel_snow_cover.return_value = {
        "image": "mocked_sentinel_image",
        "vis_param": {"mock": "vis"},
        "legend": {"mock": "legend"}
    }
    
    # Mock EarthEngineMaps.get_mapid
    mock_get_mapid = mocker.patch("api.snow.maps.get_mapid")
    mock_get_mapid.return_value = {"url": "https://mocked_sentinel.url/mapid"}
    
    response = client.get("/apiv0/snow/global_snow_cover?dataset=sentinel")
    assert response.status_code == 200
    data = response.json()
    assert data["url"] == "https://mocked_sentinel.url/mapid"
    # Sentinel usually has predefined vis_params in api.snow
    assert "vis_params" in data
    assert data["legend"] == {"mock": "legend"}
    assert data["resolution"] == "high"

def test_snow_cover_sentinel_exception(mocker):
    """Test exception handling for Sentinel."""
    mock_get_sentinel_snow_cover_composite = mocker.patch("api.snow.sentinelproducts.get_sentinel_snow_cover_composite")
    mock_get_sentinel_snow_cover_composite.side_effect = Exception("Sentinel API failed")
    
    response = client.get("/apiv0/snow/global_snow_cover?dataset=sentinel")
    assert response.status_code == 500
    assert response.json() == {"error": "Sentinel API failed"}

def test_snow_cover_invalid_dataset():
    """Test with an invalid dataset, should return None/Empty by default handler in snow.py."""
    response = client.get("/apiv0/snow/global_snow_cover?dataset=invalid")
    assert response.status_code == 200 # Since it returns None which maps to null response or nothing
    assert response.json() is None
