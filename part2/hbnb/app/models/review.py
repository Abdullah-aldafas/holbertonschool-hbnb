#!/usr/bin/python3

from datetime import datetime
import uuid
from app.models.user import User
from app.models.place import Place

class Review:
    def __init__(self, text: str, rating: int, place: Place, user: User,
                 id: str = None,
                 created_at: datetime = None,
                 updated_at: datetime = None):
        self.id = id or str(uuid.uuid4())
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

        if not text or not str(text).strip():
            raise ValueError("text is required")
        self.text = str(text).strip()

        try:
            rating = int(rating)
        except (TypeError, ValueError):
            raise ValueError("rating must be an integer")
        if not (1 <= rating <= 5):
            raise ValueError("rating must be between 1 and 5")
        self.rating = rating

        if not isinstance(place, Place):
            raise TypeError("place must be a Place instance")
        if not isinstance(user, User):
            raise TypeError("user must be a User instance")

        self.place = place
        self.user = user
