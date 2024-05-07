from time import sleep

from business_logic.dto import OperationDTO
from business_logic.services import (
    get_all_operation_paginate,
    get_operation,
    delete_operation,
    update_operation
)
from business_logic.exceptions import OperationDoesNotExistError

def main():

    main_menu = (
        'Main menu\n1 - Check balance\n2 - View transactions\n3 - Add a new '
        'transaction\nYour choice: '
    )
    while True:
        choice = input(main_menu)

        if choice == '2':
            page_number = 1
            operation_text, ids = get_all_operation_paginate(page_number=page_number)
            choice = input(operation_text)
            while choice in ('prev', 'next'):
                if choice == 'prev':
                    page_number -= 1
                else:
                    page_number += 1

                operation_text, ids = get_all_operation_paginate(page_number=page_number)
                choice = input(operation_text)
            
            if int(choice) in (range(1, len(ids) + 1)):
                operation_id = ids[int(choice) - 1]
                try:
                    operation_text = get_operation(operation_id=operation_id)
                except OperationDoesNotExistError as err:
                    print('[ERR] ' + err)
                    break
                choice = input(operation_text)

                if choice == '1':
                    try:
                        operation_text = delete_operation(operation_id=operation_id)
                    except OperationDoesNotExistError as err:
                        print('[ERR] ' + err)
                        break
                    print(operation_text)
                    sleep(2)
                    continue

                elif choice == '2':
                    category = input(
                        '\n=== Category ===\nEnter "income", "expense", or leave the '
                        'field empty to leave it unchanged.\n'
                    )
                    amount = input(
                        '\n=== Amount ===\nEnter the amount (positive number, 1 - 1.000.000) or leave '
                        'the field empty to leave it unchanged.\n'
                    )
                    description = input(
                        '\n=== Description ===\nEnter a description '
                        '(up to 50 characters) or leave the field empty to '
                        'leave it unchanged.\n'
                    )
                    data = OperationDTO(
                        category=category,
                        amount=amount,
                        description=description
                    )
                    try:
                        operation_text = update_operation(
                            operation_id=operation_id, data=data
                        )
                    except OperationDoesNotExistError as err:
                        print('[ERR] ' + err)
                        break
                    print(operation_text)
                    sleep(2)
                    continue

                elif choice == '3':
                    continue

                
                    




main()