from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from math import ceil
from datetime import datetime

if TYPE_CHECKING:
    from uuid import UUID
    from business_logic.dto import OperationDTO
    from data_access.dao import DBJsonDAO

from data_access.dao import db_provider
from data_access.exceptions import RecordDoesNotExistError
from business_logic.exceptions import OperationDoesNotExistError

from config import DB_NAME, DB_EXTENSION


dao = db_provider(DB_NAME, DB_EXTENSION)


def get_all_operation_paginate(
    per_page: int = 5,
    page_number: int = 1,
    filter: Optional[tuple[str, str | float]] = None,
    dao: DBJsonDAO = dao,
) -> tuple[str, list[str], set[Optional[str]]]:
    """
    Retrieve a paginated list of all operations from the database.

    Args:
        per_page (int): Number of operations per page (default is 5).
        page_number (int): Page number (default is 1).
        filter (Optional[tuple[str, str | float]]): Optional filter for operations.
        dao (DBJsonDAO, optional): Database access object. Defaults to dao.

    Returns:
        tuple[str, list[str], set[Optional[str]]]: A tuple containing:
            - A formatted text representing the operations for display.
            - List of operation IDs for the current page.
            - Set of buttons for navigation (e.g., 'prev', 'next').

    Raises:
        Any exceptions raised by `dao.read()`.
    """

    operations = dao.read(filter=filter)

    pages: int = ceil(len(operations) / per_page)

    result_text: str = "\n------------------------------------\n"

    start_index: int = (page_number - 1) * per_page
    end_index: int = start_index + per_page

    ids = list(operations.keys())[start_index:end_index]

    for index, operation_id in enumerate(ids):
        spaces = " " * len(str(index + 1))
        operation = operations.get(operation_id)
        date = datetime.strptime(operation.get("date"), "%Y-%m-%dT%H:%M:%S.%f")

        result_text += (
            f"{index + 1} - Date: {date.strftime('%d-%m-%Y %H:%M:%S')}\n"
            f"{spaces}   Category: {operation.get('category')}\n"
            f"{spaces}   Amount: {operation.get('amount')}\n"
            f"{spaces}   Description: {operation.get('description')}\n"
            f"------------------------------------\n"
        )

    if not ids:
        result_text += "No operations found.\n"

    buttons = set()

    result_text += "\n0 - Back to main menu\n"

    if page_number > 1:
        result_text += "\nprev   "
        buttons.add("prev")
    else:
        result_text += "\n-   "

    result_text += f"{page_number}/{pages}   "
    if page_number < pages:
        result_text += "next"
        buttons.add("next")
    else:
        result_text += "-"

    result_text += f'\n\nEnter {'"next", ' if "next" in buttons else ''}{'"prev", ' if "prev" in buttons else ''}the number of the operation you are interested in: '
    return result_text, ids, buttons


def get_operation(operation_id: UUID, dao: DBJsonDAO = dao) -> Optional[str]:
    """
    Retrieve details of a specific operation by its ID.

    Args:
        operation_id (UUID): The unique identifier of the operation.
        dao (DBJsonDAO, optional): Database access object. Defaults to dao.

    Returns:
        Optional[str]: A formatted text representing the operation details for display or None.

    Raises:
        OperationDoesNotExistError: If the operation with the specified ID does not exist.
    """
    try:
        operation = dao.read(operation_id=operation_id)

        result_text: str = (
            f"\n------------------------------------"
            f"\nDate: {operation.date.strftime('%d-%m-%Y %H:%M:%S')}\n"
            f"Category: {operation.category}\n"
            f"Amount: {operation.amount}\n"
            f"Description: {operation.description}\n"
            f"------------------------------------\n"
            f"1 - Delete operation\n2 - Modify operation\n3 - Go back\n"
            f"Your choice: "
        )

        return result_text

    except RecordDoesNotExistError:
        raise OperationDoesNotExistError(
            f"Operation with ID {operation_id} does not exits."
        )


def delete_operation(
    operation_id: UUID, dao: DBJsonDAO = dao
) -> Optional[str]:
    """
    Delete an operation from the database based on its ID.

    Args:
        operation_id (UUID): The unique identifier of the operation to delete.
        dao (DBJsonDAO, optional): Database access object. Defaults to dao.

    Returns:
        Optional[str]: A message indicating the success of the operation.

    Raises:
        OperationDoesNotExistError: If the operation with the specified ID does not exist.
    """
    try:
        dao.delete(operation_id=operation_id)
        return "\n=== Operation successfully deleted ===\n"

    except RecordDoesNotExistError:
        raise OperationDoesNotExistError(
            f"Operation with ID {operation_id} does not exits."
        )


def update_operation(
    operation_id: UUID, data: OperationDTO, dao: DBJsonDAO = dao
) -> Optional[str]:
    """
    Update an existing operation in the database.

    Args:
        operation_id (UUID): The unique identifier of the operation to update.
        data (OperationDTO): The new data for the operation.
        dao (DBJsonDAO, optional): Database access object. Defaults to dao.

    Returns:
        Optional[str]: A message indicating the success of the operation.

    Raises:
        OperationDoesNotExistError: If the operation with the specified ID does not exist.
    """
    try:
        dao.update(operation_id=operation_id, data=data)
        return "\n=== Operation successfully updated ===\n"

    except RecordDoesNotExistError:
        raise OperationDoesNotExistError(
            f"Operation with ID {operation_id} does not exits."
        )


def create_operation(data: OperationDTO, dao: DBJsonDAO = dao) -> None:
    """
    Create a new operation in the database.

    Args:
        data (OperationDTO): The data for the new operation.
        dao (DBJsonDAO, optional): Database access object. Defaults to dao.
    """
    dao.create(data=data)
