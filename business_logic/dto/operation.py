from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Optional


@dataclass
class OperationDTO:
    category: str
    amount: float
    description: str
    id: Optional[UUID] = None
    date: Optional[datetime] = None
