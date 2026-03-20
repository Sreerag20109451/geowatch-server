import pytest
from earthengine.auth import EarthEngineAuth
from earthengine.map import EarthEngineMaps
from earthengine.modis.snow import ModisProducts
from earthengine.sentinel.sentinel import SentinelProducts

def test_earthengine_auth(mocker):
    """Test EarthEngineAuth initialization logic."""
    # Note: ee is already globally mocked in conftest, so this won't hit Google APIs
    auth = EarthEngineAuth()
    
    mock_credentials = mocker.patch("earthengine.auth.ee.ServiceAccountCredentials")
    mock_initialize = mocker.patch("earthengine.auth.ee.Initialize")

    auth.initialize_earth_engine("test_account", "test_path")

    mock_credentials.assert_called_once_with("test_account", "test_path")
    mock_initialize.assert_called_once()

def test_earthengine_maps(mocker):
    """Test EarthEngineMaps get_mapid."""
    maps = EarthEngineMaps()
    
    # Mock ee.Image and its getMapId method
    mock_image = mocker.MagicMock()
    mock_image.getMapId.return_value = {"mapid": "test_id", "urlFormat": "http://test.url"}
    
    result = maps.get_mapid(mock_image, {"min": 0, "max": 100})
    assert result["mapobj"]["mapid"] == "test_id"
    assert result["url"] == "https://earthengine.googleapis.com/v1/test_id/tiles/{z}/{x}/{y}"

def test_modis_snow_cover(mocker):
    """Test ModisProducts.get_modis_snow_cover()"""
    mocker.patch("earthengine.auth.ee.ServiceAccountCredentials")
    mocker.patch("earthengine.auth.ee.Initialize")
    
    product = ModisProducts()
    
    # Mock Earth Engine objects that get chained together during Modis logic
    mock_image_collection = mocker.patch("earthengine.modis.snow.ee.ImageCollection")
    mock_collection_instance = mocker.MagicMock()
    
    # Chain filters and mapping
    mock_collection_instance.filterDate.return_value = mock_collection_instance
    mock_collection_instance.map.return_value = mock_collection_instance
    mock_collection_instance.mosaic.return_value = mock_collection_instance
    # When select is called, return another mock image
    mock_image = mocker.MagicMock()
    mock_collection_instance.select.return_value = mock_image
    
    mock_image_collection.return_value = mock_collection_instance
    
    mock_ee_number = mocker.patch("earthengine.modis.snow.ee.Number")
    
    # The actual functionality doesn't crash if we mock everything properly
    result = product.get_modis_snow_cover(
        vis_params={"min": 0, "max": 100, "palette": ["red", "green", "blue"]},
        delta=10,
        region="uk",
        is_png=False,
        qa_mask="default",
        snow_class_mask="default",
        threshold=50
    )
    
    assert "image" in result
    assert "vis_param" in result
    assert "legend" in result

def test_sentinel_snow_cover(mocker):
    """Test SentinelProducts.get_sentinel_snow_cover_composite()"""
    mocker.patch("earthengine.auth.ee.ServiceAccountCredentials")
    mocker.patch("earthengine.auth.ee.Initialize")
    
    product = SentinelProducts()
    
    # Mock Earth Engine objects
    mock_image_collection = mocker.patch("earthengine.sentinel.sentinel.ee.ImageCollection")
    mock_collection_instance = mocker.MagicMock()
    
    mock_collection_instance.filterDate.return_value = mock_collection_instance
    mock_collection_instance.filterBounds.return_value = mock_collection_instance
    mock_collection_instance.map.return_value = mock_collection_instance
    # median and select
    mock_collection_instance.median.return_value = mock_collection_instance
    
    # For calculation expressions
    mock_image = mocker.MagicMock()
    mock_image.expression.return_value = mock_image
    mock_image.addBands.return_value = mock_image
    mock_image.rename.return_value = mock_image
    mock_image.updateMask.return_value = mock_image
    
    mock_collection_instance.select.return_value = mock_image
    
    mock_image_collection.return_value = mock_collection_instance
    
    mocker.patch("earthengine.sentinel.sentinel.ee.Date")
    mocker.patch("earthengine.sentinel.sentinel.ee.FeatureCollection")
    
    # Need to return an expression when executing addBands which modifies the image.
    mock_image.expression.return_value = mock_image
    
    result = product.get_sentinel_snow_cover_composite(
        region="uk",
        threshold=0.5,
        sentnel_cloud_mask=True
    )
    
    assert "image" in result
    assert "legend" in result
