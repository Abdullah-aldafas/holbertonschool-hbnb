#!/usr/bin/python3

from datetime import datetime
from app.models.base_model import BaseModel
from app import bcrypt

class User(BaseModel):
    def __init__(self,first_name: str,last_name:str,email:str,
    is_admin: bool= False,
    id: str = None,
    created_at: datetime = None,
    updated_at: datetime = None,
    password: str = None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)

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

        # Store hashed password (if provided, hash on init)
        self.password = None
        if password:
            self.hash_password(password)

        self.places = []

    def add_place(self, place):
        """Add a place to the user's owned places"""
        self.places.append(place)

    def update(self, data):
        """Update the attributes of the object"""
        super().update(data)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        if password is None:
            return
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        if not self.password:
            return False
        return bcrypt.check_password_hash(self.password, password)