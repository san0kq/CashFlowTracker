from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from math import ceil

if TYPE_CHECKING:
    from uuid import UUID
    from business_logic.dto import OperationDTO

from data_access.dao import db_provider
from data_access.exceptions import RecordDoesNotExistError
from business_logic.exceptions import OperationDoesNotExistError

from config import DB_NAME, DB_EXTENSION


dao = db_provider(DB_NAME, DB_EXTENSION)

def get_all_operation_paginate(per_page: int = 5, page_number: int = 1) -> tuple[str, list[str]]:
    operations = dao.read()

    pages = ceil(len(operations) / per_page)

    result_text = ''

    start_index = (page_number - 1) * per_page
    end_index = start_index + per_page

    ids = list(operations.keys())[start_index:end_index]

    for index, operation_id in enumerate(ids):
        spaces = ' ' * len(str(index + 1))
        operation = operations.get(operation_id)

        result_text += (
            f'{index + 1} - Date: {operation.get('date')}\n'
            f'{spaces}   Category: {operation.get('category')}\n'
            f'{spaces}   Amount: {operation.get('amount')}\n'
            f'{spaces}   Description: {operation.get('description')}\n'
            f'------------------------------------\n'
        )
    
    if page_number > 1:
        result_text += '\nprev   '
    else:
        result_text += '\n-   '
    
    result_text += f'{page_number}/{pages}   '
    if page_number < pages:
        result_text += 'next'
    else:
        result_text += '-'

    result_text += '\n\nEnter "next", "prev" or the number of the operation you are interested in: '
    return result_text, ids


def get_operation(operation_id: UUID):
    try:
        operation = dao.read(operation_id=operation_id)

        result_text = (
            f'\n------------------------------------'
            f'\nDate: {operation.date}\n'
            f'Category: {operation.category}\n'
            f'Amount: {operation.amount}\n'
            f'Description: {operation.description}\n'
            f'------------------------------------\n'
            f'1 - Delete operatoin\n2 - Modify operation\n3 - Go back\n'
            f'Your choice: '
        )

        return result_text

    except RecordDoesNotExistError:
        raise OperationDoesNotExistError(
            f'Operation with ID {operation_id} does not exits.'
        )


def delete_operation(operation_id: UUID) -> Optional[str]:
    try:
        dao.delete(operation_id=operation_id)
        return '\n !!! Operation successfully deleted !!!\n'

    except RecordDoesNotExistError:
        raise OperationDoesNotExistError(
            f'Operation with ID {operation_id} does not exits.'
        )


def update_operation(operation_id: UUID, data: OperationDTO) -> Optional[str]:
    try:
        dao.update(operation_id=operation_id, data=data)
        return '\n !!! Operation successfully updated !!!\n'

    except RecordDoesNotExistError:
        raise OperationDoesNotExistError(
            f'Operation with ID {operation_id} does not exits.'
        )
