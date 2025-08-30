#!/usr/bin/python3

from datetime import datetime
import uuid
from app.models.user import User

class Place:
    def __init__(self, title: str, description: str, price: float,
                 latitude: float, longitude: float, owner: User,
                 id: str = None,
                 created_at: datetime = None,
                 updated_at: datetime = None):
        self.id = id or str(uuid.uuid4())
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

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

        if not isinstance(owner, User):
            raise TypeError("owner must be a User instance")
        self.owner = owner

        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def update(self, data):
        """Update the attributes of the object"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp