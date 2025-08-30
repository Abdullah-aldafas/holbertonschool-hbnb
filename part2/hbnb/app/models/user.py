#!/usr/bin/python3

from datetime import datetime
import uuid

class User:
    def __init__(self,first_name: str,last_name:str,email:str,
    is_admin: bool= False,
    id: str = None,
    created_at: datetime = None,
    updated_at: datetime = None):
        self.id = id or str(uuid.uuid4())

        if not first_name or len(first_name) > 50:
            raise ValueError("first_name must be at most 50 characters")
        self.first_name = first_name.strip()
        if not last_name or len(last_name) > 50:
            raise ValueError("last_name must be at most 50 characters")
        self.last_name = last_name.strip()

        if "@" not in email or "." not in email:
            raise ValueError("Invalid email address")
        self.email = email.strip().lower()

        self.is_admin = bool(is_admin)

        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

        self.places = []

    def add_place(self, place):
        """Add a place to the user's owned places"""
        self.places.append(place)

    def update(self, data):
        """Update the attributes of the object"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp