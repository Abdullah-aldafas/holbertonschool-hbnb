import unittest
from app import create_app
class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
    # ---------- USERS ----------
    def test_create_user_success(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
    def test_create_user_invalid(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid"
        })
        self.assertEqual(response.status_code, 400)
    # ---------- PLACES ----------
    def test_create_place_success(self):
        user = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "One",
            "email": "owner@example.com"
        }).get_json()
        owner_id = user["id"]
        response = self.client.post('/api/v1/places/', json={
            "title": "Villa",
            "description": "Nice place",
            "price": 120,
            "latitude": 25.0,
            "longitude": 45.0,
            "owner_id": owner_id,
            "amenity_ids": []
        })
        self.assertEqual(response.status_code, 201)
    def test_create_place_invalid_price(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Bad Place",
            "description": "Invalid price",
            "price": -50,
            "latitude": 25.0,
            "longitude": 45.0,
            "owner_id": "fake",
            "amenity_ids": []
        })
        self.assertEqual(response.status_code, 400)
    # ---------- REVIEWS ----------
    def test_create_review_invalid_rating(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Bad rating",
            "rating": 10,
            "user_id": "fake",
            "place_id": "fake"
        })
        self.assertEqual(response.status_code, 400)
if __name__ == '__main__':
    unittest.main()
