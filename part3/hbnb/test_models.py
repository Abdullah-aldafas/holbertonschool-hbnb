
import unittest
from app.services.facade import HBnBFacade


class TestModels(unittest.TestCase):
    def setUp(self):
        self.facade = HBnBFacade()

    def test_create_user_success(self):
        user = self.facade.create_user({
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com"
        })
        self.assertEqual(user.email, "jane@example.com")

    def test_create_user_duplicate_email(self):
        self.facade.create_user({
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "duplicate@example.com"
        })
        with self.assertRaises(ValueError):
            self.facade.create_user({
                "first_name": "Other",
                "last_name": "User",
                "email": "duplicate@example.com"
            })

    def test_create_place_invalid_latitude(self):
        user = self.facade.create_user({
            "first_name": "Owner",
            "last_name": "One",
            "email": "owner2@example.com"
        })
        with self.assertRaises(ValueError):
            self.facade.create_place({
                "title": "Villa",
                "description": "Nice",
                "price": 100,
                "latitude": 200,  # invalid
                "longitude": 45,
                "owner_id": user.id,
                "amenities": []
            })

    def test_create_review_invalid_text(self):
        user = self.facade.create_user({
            "first_name": "Reviewer",
            "last_name": "One",
            "email": "reviewer@example.com"
        })
        place = self.facade.create_place({
            "title": "Spot",
            "description": "Cool",
            "price": 50,
            "latitude": 25,
            "longitude": 45,
            "owner_id": user.id,
            "amenities": []
        })
        with self.assertRaises(ValueError):
            self.facade.create_review({
                "text": "",
                "rating": 3,
                "user_id": user.id,
                "place_id": place.id
            })


if __name__ == '__main__':
    unittest.main()
