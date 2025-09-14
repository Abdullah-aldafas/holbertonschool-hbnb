#!/usr/bin/python3

from datetime import datetime
from app.models.base_model import BaseModel
from typing import Optional

class Review(BaseModel):
    def __init__(self, text: str, rating: int, place_id: str, user_id: str,
                 id: Optional[str] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)

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

        if not place_id or not str(place_id).strip():
            raise ValueError("place_id is required")
        if not user_id or not str(user_id).strip():
            raise ValueError("user_id is required")
        self.place_id = str(place_id).strip()
        self.user_id = str(user_id).strip()

    def update(self, data):
        """Update the attributes of the object"""
        super().update(data)
