#!/usr/bin/python3

from datetime import datetime
from app.models.base_model import BaseModel
from typing import List

class Place(BaseModel):
    def __init__(self, title: str, description: str, price: float,
                 latitude: float, longitude: float, owner_id: str,
                 amenities: List[str] = None,
                 id: str = None,
                 created_at: datetime = None,
                 updated_at: datetime = None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)

        if not title or len(title.strip()) > 100:
            raise ValueError("title must be at most 100 characters")
        self.title = title.strip()

        self.description = (description or "").strip()

        try:
            price = float(price)
        except (TypeError, ValueError):
            raise ValueError("price must be a number")
        if price <= 0:
            raise ValueError("price must be positive")
        self.price = price

        self.latitude = float(latitude)
        if not (-90.0 <= self.latitude <= 90.0):
            raise ValueError("latitude must be between -90 and 90")

        
        self.longitude = float(longitude)
        if not (-180.0 <= self.longitude <= 180.0):
            raise ValueError("longitude must be between -180 and 180")

        if not owner_id or not str(owner_id).strip():
            raise ValueError("owner_id is required")
        self.owner_id = str(owner_id).strip()

        self.reviews = []  # list of review IDs (optional future use)
        self.amenities = [str(aid) for aid in (amenities or [])]

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity_id: str):
        """Add an amenity id to the place."""
        self.amenities.append(str(amenity_id))

    def update(self, data):
        """Update the attributes of the object"""
        super().update(data)