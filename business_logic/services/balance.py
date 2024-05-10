from __future__ import annotations

from typing import TYPE_CHECKING

from data_access.dao import db_provider

if TYPE_CHECKING:
    from data_access.dao import DBJsonDAO


from config import DB_NAME, DB_EXTENSION


dao = db_provider(DB_NAME, DB_EXTENSION)


def get_balance(dao: DBJsonDAO = dao) -> float:
    """
    Calculate the balance based on income and expense operations.

    Returns:
        float: The calculated balance.

    Raises:
        Any exceptions raised by `dao.read()`.
    """
    operations = dao.read()

    balance: float = 0.0

    for operation in operations:
        amount = operations[operation]["amount"]
        if operations[operation]["category"] == "income":
            balance += amount
        else:
            balance -= amount

    return balance
