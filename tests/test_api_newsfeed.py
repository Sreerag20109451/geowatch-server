import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_dailynews_success(mocker):
    """Test successful retrieval of daily news."""
    # Since get_daily_news_from_redis is an async function, we need an AsyncMock
    mock_get_news = mocker.patch("api.newsfeed.newsfeed.get_daily_news_from_redis")
    
    # The endpoint expects the structure {"news": [items...]}
    mock_get_news.return_value = {
        "news": [{"title": "Test Title", "content": "Test Content", "href": "http://test.com"}]
    }

    response = client.get("/apiv0/newsfeed/getdailynews")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "success"
    assert data["data"] == [{"title": "Test Title", "content": "Test Content", "href": "http://test.com"}]

def test_get_dailynews_exception(mocker):
    """Test exception handling in daily news retrieval."""
    mock_get_news = mocker.patch("api.newsfeed.newsfeed.get_daily_news_from_redis")
    mock_get_news.side_effect = Exception("Redis error")
    
    response = client.get("/apiv0/newsfeed/getdailynews")
    assert response.status_code == 500
    data = response.json()
    assert data["message"] == "Error retrieving data: Redis error"
