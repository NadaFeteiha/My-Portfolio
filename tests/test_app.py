import unittest
import os
os.environ['TESTING'] = 'true'

from app import create_app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        #Remember to add a title and then update the test because I believe you did not add a title
        assert "<title></title>" in html
        # Extra home page test: check that certain text exists
        assert "Software" in html or "MLH" in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json

         # Test POST /api/timeline_post
        post_response = self.client.post("/api/timeline_post", data={
            "name": "Test User",
            "email": "test@example.com",
            "content": "This is a test post"
        })
        assert post_response.status_code == 200
        post_json = post_response.get_json()
        assert post_json["name"] == "Test User"
        assert post_json["email"] == "test@example.com"
        assert post_json["content"] == "This is a test post"

        # Test GET /api/timeline_post after adding a post
        get_response = self.client.get("/api/timeline_post")
        assert get_response.status_code == 200
        get_json = get_response.get_json()
        assert len(get_json["timeline_posts"]) == 1

        # Test timeline page (frontend)
        timeline_page = self.client.get("/timeline")
        assert timeline_page.status_code == 200
        page_html = timeline_page.get_data(as_text=True)
        assert "Timeline" in page_html or "Post" in page_html

    def test_malformed_timeline_post(self):
    # POST request missing name
        response = self.client.post("/api/timeline_post", data={
            "email": "john@example.com", 
            "content": "Hello world, I'm John!"
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe", 
            "email": "john@example.com", 
            "content": ""
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe", 
            "email": "not-an-email", 
            "content": "Hello world, I'm John!"
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html


