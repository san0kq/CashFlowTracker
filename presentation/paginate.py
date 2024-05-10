from time import sleep

from business_logic.dto import OperationDTO
from business_logic.exceptions import OperationDoesNotExistError
from business_logic.services import (
    delete_operation,
    get_all_operation_paginate,
    get_operation,
    update_operation,
)
from presentation.validators import (
    validate_user_choice,
    validate_amount,
    validate_category,
    validate_description,
)


def paginate_operation(filter: tuple[str, str | float] = None) -> None:
    """
    Paginate and interact with operations based on provided filter.

    Args:
        filter (tuple[str, str | float], optional): A filter tuple (key, value) to filter operations. Defaults to None.
    """
    page_number: int = 1
    operation_text, ids, buttons = get_all_operation_paginate(
        page_number=page_number, filter=filter
    )
    operation_choice: str = input(operation_text)
    validate_user_choice(
        choice=operation_choice, max_choice=len(ids), buttons=buttons
    )
    while operation_choice in ("prev", "next"):
        if operation_choice == "prev":
            page_number -= 1
        else:
            page_number += 1

        operation_text, ids, buttons = get_all_operation_paginate(
            page_number=page_number, filter=filter
        )
        operation_choice = input(operation_text)
        validate_user_choice(
            choice=operation_choice, max_choice=len(ids), buttons=buttons
        )

    if operation_choice == "0":
        return

    if int(operation_choice) in (range(1, len(ids) + 1)):
        operation_id = ids[int(operation_choice) - 1]
        try:
            operation_text = get_operation(operation_id=operation_id)
        except OperationDoesNotExistError as err:
            print("[ERR] " + err)
            return
        operation_choice = input(operation_text)
        validate_user_choice(choice=operation_choice, max_choice=3)

        if operation_choice == "1":
            try:
                operation_text = delete_operation(operation_id=operation_id)
            except OperationDoesNotExistError as err:
                print("[ERR] " + err)
                return
            print(operation_text)
            sleep(2)
            return

        elif operation_choice == "2":
            category = input(
                '\n=== Category ===\nEnter "income", "expense", or leave the '
                "field empty to leave it unchanged.\n"
            )
            if category:
                validate_category(category=category)

            amount = input(
                "\n=== Amount ===\nEnter the amount (positive number, 1 - 1.000.000) or leave "
                "the field empty to leave it unchanged.\n"
            )
            if amount:
                validate_amount(amount=amount)

            description = input(
                "\n=== Description ===\nEnter a description "
                "(up to 50 characters) or leave the field empty to "
                "leave it unchanged.\n"
            )
            if description:
                validate_description(description=description)

            data = OperationDTO(
                category=category,
                amount=float(amount),
                description=description,
            )
            try:
                operation_text = update_operation(
                    operation_id=operation_id, data=data
                )
            except OperationDoesNotExistError as err:
                print("[ERR] " + err)
                return
            print(operation_text)
            sleep(2)
            return

        elif operation_choice == "3":
            return
