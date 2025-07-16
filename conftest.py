import pytest
import requests

@pytest.fixture
def base_url():
    """Base URL for JSONPlaceholder API"""
    return "https://jsonplaceholder.typicode.com"

@pytest.fixture
def session():
    """HTTP session for making requests"""
    return requests.Session()

@pytest.fixture
def valid_post_data():
    """Valid post data for testing POST requests"""
    return {
        "title": "Test Post",
        "body": "This is a test post body",
        "userId": 1
    }

@pytest.fixture
def expected_post_keys():
    """Expected keys in a post response"""
    return {"userId", "id", "title", "body"}

@pytest.fixture
def expected_user_keys():
    """Expected keys in a user response"""
    return {"id", "name", "username", "email", "address", "phone", "website", "company"}