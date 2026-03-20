import pytest
import os
import sys
from unittest import mock
import redis

# Set environment variables BEFORE any modules are imported to prevent initialization errors
os.environ["SERVICE_ACCOUNT"] = "test-account@test.iam.gserviceaccount.com"
os.environ["KEY_JSON"] = '{"type": "service_account", "project_id": "test"}'
os.environ["REDIS_URL"] = "redis://localhost:6379/0"
os.environ["UPSTASH_REDIS_REST_URL"] = "https://test.upstash.io"
os.environ["UPSTASH_REDIS_REST_TOKEN"] = "test_token"
os.environ["NEWSDATA_API_KEY"] = "test_news_api_key"

# We must patch these at import time because `main.py` evaluates them at module level.
mock_redis = mock.patch("redis.from_url")
mock_redis.start()

import sys
from unittest import mock
sys.modules["ee"] = mock.MagicMock()

@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Ensure environment variables are consistently mocked for all tests."""
    monkeypatch.setenv("SERVICE_ACCOUNT", "test-account@test.iam.gserviceaccount.com")
    monkeypatch.setenv("KEY_JSON", '{"type": "service_account", "project_id": "test"}')
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379/0")
    monkeypatch.setenv("UPSTASH_REDIS_REST_URL", "https://test.upstash.io")
    monkeypatch.setenv("UPSTASH_REDIS_REST_TOKEN", "test_token")
    monkeypatch.setenv("NEWSDATA_API_KEY", "test_news_api_key")

