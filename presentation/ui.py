from time import sleep
from datetime import datetime

from business_logic.dto import OperationDTO
from business_logic.services import (
    get_balance,
    create_operation,
)
from presentation.paginate import paginate_operation
from presentation.validators import (
    validate_user_choice,
    validate_category,
    validate_amount,
    validate_description,
    validate_date,
)
from presentation.exceptions import (
    UserChoiceError,
    DateError,
    DescriptionError,
    AmountError,
    CategoryError,
)


def ui_func() -> None:
    """
    User interface function for interacting with the application.

    This function continuously prompts the user with a main menu and handles user inputs accordingly.
    It allows the user to perform various operations such as checking balance, viewing operations,
    adding new operations, and finding operations based on different criteria.
    """
    main_menu: str = (
        "------------------------------------"
        "\nMain menu\n1 - Check balance\n2 - View operations\n3 - Add a new "
        "operation\n4 - Find a operation\n0 - Exit\nYour choice: "
    )
    while True:
        choice: str = input(main_menu)

        try:
            validate_user_choice(choice=choice, max_choice=5)
        except UserChoiceError as err:
            print(f"\n!!! {err} !!!\n")
            sleep(2)
            continue

        if choice == "1":
            balance: float = get_balance()
            print(
                f"\n------------------------------------"
                f"\n=== Your balance: {balance} ==="
            )
            sleep(2)
            continue

        if choice == "2":
            try:
                paginate_operation()
            except (
                UserChoiceError,
                DescriptionError,
                CategoryError,
                AmountError,
            ) as err:
                print(f"\n!!! {err} !!!\n")
                sleep(2)
                continue

        if choice == "3":
            try:
                category: str = input(
                    "\n------------------------------------"
                    '\nTo add a new operation, enter its category ("income" or "expense"): '
                )
                validate_category(category=category)

                amount: str = input(
                    "Enter the amount (positive number, 1 - 1.000.000): "
                )
                validate_amount(amount=amount)

                description: str = input(
                    "Enter a description (up to 50 characters): "
                )
                validate_description(description=description)
            except (CategoryError, AmountError, DescriptionError) as err:
                print(f"\n!!! {err} !!!\n")
                sleep(2)
                continue

            create_operation(
                OperationDTO(
                    category=category,
                    amount=float(amount),
                    description=description,
                )
            )
            print(
                "\n------------------------------------"
                "\n=== The operation has been successfully added. ==="
            )

        if choice == "4":
            try:
                find_choice: str = input(
                    "\n------------------------------------"
                    "\nFind operation by:\n1 - Category\n2 - Date\n3 - Amount\nYour choice: "
                )
                validate_user_choice(choice=find_choice, max_choice=3)

                if find_choice == "1":
                    filter_key: str = "category"
                    filter_value: str = input(
                        'Enter the category of the operation you are interested in ("income" or "expense"): '
                    )
                    validate_category(category=filter_value)

                elif find_choice == "2":
                    filter_key: str = "date"
                    input_date: str = input(
                        "Please enter the date you are interested in, in the format DD-MM-YYYY: "
                    )
                    validate_date(date=input_date)
                    filter_value: datetime = datetime.strptime(
                        input_date, "%d-%m-%Y"
                    )

                elif find_choice == "3":
                    filter_key: str = "amount"
                    filter_value: str = input(
                        "Enter the amount (positive number, 1 - 1.000.000): "
                    )
                    validate_amount(amount=filter_value)
                    filter_value: float = float(filter_value)

                paginate_operation(filter=(filter_key, filter_value))

            except (
                UserChoiceError,
                DateError,
                DescriptionError,
                CategoryError,
                AmountError,
            ) as err:
                print(f"\n!!! {err} !!!\n")
                sleep(2)
                continue

        if choice == "0":
            break
