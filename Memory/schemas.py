# schemas.py

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Message:
    role: str
    content: str
    created_at: datetime


@dataclass
class Session:
    id: str
    summary: str
    created_at: datetime