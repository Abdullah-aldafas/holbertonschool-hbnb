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

        if not name or len(name.strip()) > 50:
            raise ValueError("name must be at most 50 characters")
        self.name = name.strip()
