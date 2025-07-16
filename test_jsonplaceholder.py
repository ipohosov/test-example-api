import pytest
import requests
import time
from typing import Dict, Any, List


class TestJSONPlaceholderAPI:
    """Test suite for JSONPlaceholder API endpoints"""

    @pytest.mark.parametrize("endpoint,expected_count", [
        ("/posts", 100),
        ("/users", 10),
        ("/comments", 500),
        ("/albums", 100),
        ("/photos", 5000),
    ])
    def test_get_all_resources_count(self, base_url: str, session: requests.Session,
                                     endpoint: str, expected_count: int):
        """Test GET requests for all resources return expected count"""
        response = session.get(f"{base_url}{endpoint}")

        # Status code validation
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        # Response time validation (should be under 2 seconds)
        assert response.elapsed.total_seconds() < 2.0, "Response time too slow"

        # Content type validation
        assert "application/json" in response.headers.get("content-type", "")

        # Data validation
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        assert len(data) == expected_count, f"Expected {expected_count} items, got {len(data)}"

    @pytest.mark.parametrize("post_id,should_exist", [
        (1, True),
        (50, True),
        (100, True),
        (101, False),
        (0, False),
        (-1, False),
    ])
    def test_get_specific_post(self, base_url: str, session: requests.Session,
                               expected_post_keys: set, post_id: int, should_exist: bool):
        """Test GET requests for specific posts"""
        response = session.get(f"{base_url}/posts/{post_id}")

        if should_exist:
            # Valid post ID tests
            assert response.status_code == 200, f"Expected 200 for post {post_id}"

            data = response.json()
            assert isinstance(data, dict), "Response should be a dictionary"

            # Validate required fields are present
            assert expected_post_keys.issubset(set(data.keys())), "Missing required fields"

            # Validate data types
            assert isinstance(data["userId"], int), "userId should be integer"
            assert isinstance(data["id"], int), "id should be integer"
            assert isinstance(data["title"], str), "title should be string"
            assert isinstance(data["body"], str), "body should be string"

            # Validate values
            assert data["id"] == post_id, f"Expected id {post_id}, got {data['id']}"
            assert data["userId"] > 0, "userId should be positive"
            assert len(data["title"]) > 0, "title should not be empty"
            assert len(data["body"]) > 0, "body should not be empty"
        else:
            # Invalid post ID tests
            assert response.status_code == 404, f"Expected 404 for invalid post {post_id}"

    @pytest.mark.parametrize("user_id,should_exist", [
        (1, True),
        (5, True),
        (10, True),
        (11, False),
        (0, False),
        (-1, False),
    ])
    def test_get_specific_user(self, base_url: str, session: requests.Session,
                               expected_user_keys: set, user_id: int, should_exist: bool):
        """Test GET requests for specific users"""
        response = session.get(f"{base_url}/users/{user_id}")

        if should_exist:
            assert response.status_code == 200, f"Expected 200 for user {user_id}"

            data = response.json()
            assert isinstance(data, dict), "Response should be a dictionary"

            # Validate required fields
            assert expected_user_keys.issubset(set(data.keys())), "Missing required user fields"

            # Validate data types and structure
            assert isinstance(data["id"], int), "id should be integer"
            assert isinstance(data["name"], str), "name should be string"
            assert isinstance(data["username"], str), "username should be string"
            assert isinstance(data["email"], str), "email should be string"
            assert isinstance(data["address"], dict), "address should be dictionary"
            assert isinstance(data["company"], dict), "company should be dictionary"

            # Validate email format
            assert "@" in data["email"], "email should contain @ symbol"
            assert "." in data["email"], "email should contain domain"

            # Validate nested address structure
            address_keys = {"street", "suite", "city", "zipcode", "geo"}
            assert address_keys.issubset(set(data["address"].keys())), "Missing address fields"

        else:
            assert response.status_code == 404, f"Expected 404 for invalid user {user_id}"

    @pytest.mark.parametrize("post_data,expected_status", [
        ({"title": "Test Post", "body": "Test Body", "userId": 1}, 201),
        ({"title": "", "body": "Test Body", "userId": 1}, 201),  # JSONPlaceholder allows empty title
        ({"title": "Test Post", "body": "", "userId": 1}, 201),  # JSONPlaceholder allows empty body
        ({}, 201),  # JSONPlaceholder allows empty data
    ])
    def test_create_post(self, base_url: str, session: requests.Session,
                         post_data: Dict[str, Any], expected_status: int):
        """Test POST requests for creating posts"""
        response = session.post(f"{base_url}/posts", json=post_data)

        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"

        if expected_status == 201:
            data = response.json()
            assert isinstance(data, dict), "Response should be a dictionary"

            # JSONPlaceholder returns an id for created posts
            assert "id" in data, "Created post should have an id"
            assert isinstance(data["id"], int), "id should be integer"

            # Verify the sent data is reflected in response
            for key, value in post_data.items():
                assert data.get(key) == value, f"Expected {key}={value}, got {data.get(key)}"

    @pytest.mark.parametrize("post_id,update_data,expected_status", [
        (1, {"title": "Updated Title", "body": "Updated Body", "userId": 1}, 200),
        (50, {"title": "Another Update"}, 200),
        (100, {"body": "Only body update"}, 200),
        (101, {"title": "Update non-existent"}, 500),  # JSONPlaceholder returns 200 even for non-existent
    ])
    def test_update_post(self, base_url: str, session: requests.Session,
                         post_id: int, update_data: Dict[str, Any], expected_status: int):
        """Test PUT requests for updating posts"""
        response = session.put(f"{base_url}/posts/{post_id}", json=update_data)

        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"

        if expected_status == 200:
            data = response.json()
            assert isinstance(data, dict), "Response should be a dictionary"

            # Verify the updated data is reflected
            for key, value in update_data.items():
                assert data.get(key) == value, f"Expected {key}={value}, got {data.get(key)}"

    @pytest.mark.parametrize("post_id,expected_status", [
        (1, 200),
        (50, 200),
        (100, 200),
        (101, 200),  # JSONPlaceholder returns 200 even for non-existent
    ])
    def test_delete_post(self, base_url: str, session: requests.Session,
                         post_id: int, expected_status: int):
        """Test DELETE requests for posts"""
        response = session.delete(f"{base_url}/posts/{post_id}")

        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"

    def test_headers_validation(self, base_url: str, session: requests.Session):
        """Test response headers validation"""
        response = session.get(f"{base_url}/posts")

        # Check essential headers
        assert "content-type" in response.headers, "Missing content-type header"
        assert "application/json" in response.headers["content-type"], "Wrong content-type"

        # Check CORS headers
        assert "access-control-allow-origin" not in response.headers, "CORS headers should be not presented"

        # Check cache headers
        assert "cache-control" in response.headers, "Missing cache-control header"

    def test_pagination_and_filtering(self, base_url: str, session: requests.Session):
        """Test pagination and filtering capabilities"""
        # Test pagination
        response = session.get(f"{base_url}/posts?_limit=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10, "Pagination limit not working"

        # Test filtering
        response = session.get(f"{base_url}/posts?userId=1")
        assert response.status_code == 200
        data = response.json()
        assert all(post["userId"] == 1 for post in data), "Filtering by userId failed"

        # Test sorting
        response = session.get(f"{base_url}/posts?_sort=id&_order=desc")
        assert response.status_code == 200
        data = response.json()
        ids = [post["id"] for post in data]
        assert ids == sorted(ids, reverse=True), "Sorting by id desc failed"
