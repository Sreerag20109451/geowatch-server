import pytest
import json
import datetime
from dailytasks.newsfeed import NewsFeed
from dailytasks.newsfeedtools import get_newsData

@pytest.fixture
def newsfeed():
    return NewsFeed()

@pytest.mark.asyncio
async def test_save_to_redis(mocker, newsfeed):
    """Test saving data to Redis using Upstash."""
    mock_redis = mocker.patch("dailytasks.newsfeed.Redis")
    mock_redis_instance = mocker.AsyncMock()
    mock_redis.return_value = mock_redis_instance

    test_data = {"news": [], "create_dtm": "2023-01-01T00:00:00"}
    await newsfeed.save_to_redis(test_data)
    
    # Assert set was called with the stringified JSON
    mock_redis_instance.set.assert_called_once_with('daily_news_feed', json.dumps(test_data))

@pytest.mark.asyncio
async def test_save_to_redis_no_url(mocker):
    """Test saving data when REDIS URL is None."""
    # Ensure URL is missing
    mocker.patch("dailytasks.newsfeed.os.getenv", return_value=None)
    newsfeed = NewsFeed()
    
    mock_redis = mocker.patch("dailytasks.newsfeed.Redis")
    test_data = {"news": []}
    result = await newsfeed.save_to_redis(test_data)
    
    assert result is None
    mock_redis.assert_not_called()

@pytest.mark.asyncio
async def test_get_daily_news_cache_hit(mocker, newsfeed):
    """Test retrieving news from cache when it's fresh."""
    mock_redis = mocker.patch("dailytasks.newsfeed.Redis")
    mock_redis_instance = mocker.AsyncMock()
    
    # Simulate fresh cache
    fresh_time = datetime.datetime.now().isoformat()
    cached_data = json.dumps({"news": [], "create_dtm": fresh_time})
    mock_redis_instance.get.return_value = cached_data
    mock_redis.return_value = mock_redis_instance
    
    mock_get_newsData = mocker.patch("dailytasks.newsfeed.get_newsData")

    result = await newsfeed.get_daily_news_from_redis()
    
    assert result["create_dtm"] == fresh_time
    mock_get_newsData.assert_not_called()

@pytest.mark.asyncio
async def test_get_daily_news_cache_expired(mocker, newsfeed):
    """Test cache invalidation - mock older than 1 day."""
    mock_redis = mocker.patch("dailytasks.newsfeed.Redis")
    mock_redis_instance = mocker.AsyncMock()
    
    # Simulate old cache
    old_time = (datetime.datetime.now() - datetime.timedelta(days=2)).isoformat()
    cached_data = json.dumps({"news": [], "create_dtm": old_time})
    mock_redis_instance.get.return_value = cached_data
    mock_redis.return_value = mock_redis_instance
    
    mock_get_newsData = mocker.patch("dailytasks.newsfeed.get_newsData", new_callable=mocker.AsyncMock)
    mock_get_newsData.return_value = {"news": [{"new": "data"}], "create_dtm": datetime.datetime.now().isoformat()}

    mock_save = mocker.patch.object(newsfeed, "save_to_redis")

    result = await newsfeed.get_daily_news_from_redis()
    
    assert "news" in result
    mock_get_newsData.assert_called_once()
    mock_save.assert_called_once()

@pytest.mark.asyncio
async def test_get_daily_news_cache_miss(mocker, newsfeed):
    """Test behavior when cache is completely missing."""
    mock_redis = mocker.patch("dailytasks.newsfeed.Redis")
    mock_redis_instance = mocker.AsyncMock()
    mock_redis_instance.get.return_value = None
    mock_redis.return_value = mock_redis_instance

    mock_get_newsData = mocker.patch("dailytasks.newsfeed.get_newsData", new_callable=mocker.AsyncMock)
    mock_get_newsData.return_value = {"news": [{"fresh": "data"}], "create_dtm": "timestamp"}
    
    mock_save = mocker.patch.object(newsfeed, "save_to_redis")

    result = await newsfeed.get_daily_news_from_redis()
    
    assert result["news"] == [{"fresh": "data"}]
    mock_get_newsData.assert_called_once()
    mock_save.assert_called_once()

def test_get_newsData_success(mocker):
    """Test get_newsData successful request."""
    mock_requests_get = mocker.patch("dailytasks.newsfeedtools.requests.get")
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = {
        "results": [
            {
                "title": "Title 1",
                "image_url": "img.png",
                "description": "Desc",
                "link": "http://link.com",
                "source_id": "source1"
            }
        ]
    }
    mock_requests_get.return_value = mock_response

    result = get_newsData()
    assert "news" in result
    assert len(result["news"]) == 1
    assert result["news"][0]["title"] == "Title 1"
    assert "create_dtm" in result

def test_get_newsData_exception(mocker):
    """Test get_newsData failure scenario."""
    mock_requests_get = mocker.patch("dailytasks.newsfeedtools.requests.get")
    mock_requests_get.side_effect = Exception("HTTP Error")

    result = get_newsData()
    assert isinstance(result, Exception)
    assert str(result) == "Error loading news data"
