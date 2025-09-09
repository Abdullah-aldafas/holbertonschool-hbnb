#!/usr/bin/python3

from datetime import datetime
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name: str,
                 id: str = None,
                 created_at: datetime = None,
                 updated_at: datetime = None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)

        if name:
            name = name.strip()
        else:
            name = ""
        if not name or len(name) > 50:
            raise ValueError("name is required and must be at most 50 characters")
        self.name = name
        

    def update(self, data):
        """Update the attributes of the object"""
        super().update(data)
