#!/usr/bin/python3

from datetime import datetime
import uuid

class Amenity:
    def __init__(self, name: str,
                 id: str = None,
                 created_at: datetime = None,
                 updated_at: datetime = None):
        self.id = id or str(uuid.uuid4())
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

        if name:
            name = name.strip()
        else:
            name = ""
        if not name or len(name) > 50:
            raise ValueError("name is required and must be at most 50 characters")
        self.name = name
        

    def update(self, data):
        """Update the attributes of the object"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp
