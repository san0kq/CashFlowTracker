from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Optional


@dataclass
class OperationDTO:
    """
    Data class representing an operation.

    Attributes:
        category (str): The category of the operation (e.g., "income" or "expense").
        amount (float): The amount of the operation.
        description (str): A brief description of the operation (max 50 characters).
        id (Optional[UUID]): Optional unique identifier for the operation.
        date (Optional[datetime]): Optional date of the operation in the format DD-MM-YYYY.
    """

    category: str
    amount: float
    description: str
    id: Optional[UUID] = None
    date: Optional[datetime] = None
