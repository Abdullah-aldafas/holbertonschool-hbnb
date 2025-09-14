#!/usr/bin/python3

from datetime import datetime
import uuid
from typing import Optional


class BaseModel:
    def __init__(self,
                 id: Optional[str] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        self.id = id or str(uuid.uuid4())
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def touch(self) -> None:
        self.updated_at = datetime.utcnow()

    def update(self, data: dict) -> None:
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.touch()


