"""
API test layer - tests the JSONPlaceholder API directly, no browser involved.
This is deliberately kept independent of the UI tests: it should run in
seconds, not minutes, which is the whole point of having an API layer.

Run just these tests with:  pytest -m api
"""

import pytest

pytestmark = pytest.mark.api


class TestPostsAPI:

    def test_get_all_posts_returns_200(self, api_client):
        response = api_client.get("/posts")
        assert response.status_code == 200
        assert len(response.json()) == 100  # JSONPlaceholder has 100 fixed posts

    def test_get_single_post_returns_correct_fields(self, api_client):
        response = api_client.get("/posts/1")
        assert response.status_code == 200

        body = response.json()
        assert body["id"] == 1
        assert "title" in body
        assert "body" in body
        assert "userId" in body

    def test_get_nonexistent_post_returns_404(self, api_client):
        response = api_client.get("/posts/9999")
        assert response.status_code == 404

    def test_create_post_returns_201(self, api_client):
        payload = {
            "title": "QA automation framework post",
            "body": "Testing the create endpoint",
            "userId": 1,
        }
        response = api_client.post("/posts", json=payload)

        assert response.status_code == 201
        body = response.json()
        assert body["title"] == payload["title"]
        assert "id" in body  # server should assign a new id

    def test_update_post_returns_200(self, api_client):
        payload = {
            "id": 1,
            "title": "Updated title",
            "body": "Updated body",
            "userId": 1,
        }
        response = api_client.put("/posts/1", json=payload)

        assert response.status_code == 200
        assert response.json()["title"] == "Updated title"

    def test_delete_post_returns_200(self, api_client):
        response = api_client.delete("/posts/1")
        assert response.status_code == 200

    @pytest.mark.parametrize("post_id", [1, 5, 10, 50, 100])
    def test_multiple_posts_have_valid_structure(self, api_client, post_id):
        """Data-driven API test: same assertion logic run across several IDs."""
        response = api_client.get(f"/posts/{post_id}")
        assert response.status_code == 200

        body = response.json()
        assert body["id"] == post_id
        assert isinstance(body["title"], str) and len(body["title"]) > 0
