from typing import Optional
from datetime import datetime

from presentation.exceptions import (
    UserChoiceError,
    AmountError,
    CategoryError,
    DescriptionError,
    DateError,
)


def validate_user_choice(
    choice: str, max_choice: int, buttons: Optional[set[Optional[str]]] = None
) -> None:
    """
    Validate user input choice.

    Args:
        choice (str): User input choice.
        max_choice (int): Maximum choice number.
        buttons (Optional[set[Optional[str]]], optional): Set of button options. Defaults to None.

    Raises:
        UserChoiceError: If the choice is invalid.
    """
    if buttons and not choice.isdigit() and choice not in buttons:
        raise UserChoiceError(
            "There is no such choice. Please select from the options provided."
        )

    if not buttons and not choice.isdigit():
        raise UserChoiceError("Choice must be a digit.")

    if choice.isdigit() and choice not in map(str, range(max_choice + 1)):
        raise UserChoiceError(
            f"Choice must be within the range of 0 to {max_choice}."
        )


def validate_category(category: str) -> None:
    """
    Validate operation category.

    Args:
        category (str): Operation category.

    Raises:
        CategoryError: If the category is invalid.
    """
    if category not in ("income", "expense"):
        raise CategoryError(
            'The category can be either "income" or "expense".'
        )


def validate_amount(amount: str) -> None:
    """
    Validate operation amount.

    Args:
        amount (str): Operation amount.

    Raises:
        AmountError: If the amount is invalid.
    """
    try:
        float(amount)
    except ValueError:
        raise AmountError(
            "The amount must be either an integer or a floating-point number."
        )

    if not 0 <= float(amount) <= 1_000_000:
        raise AmountError(
            "The amount must be a number between 0 and 1,000,000, inclusive."
        )


def validate_description(description: str) -> None:
    """
    Validate operation description.

    Args:
        description (str): Operation description.

    Raises:
        DescriptionError: If the description is invalid.
    """
    if len(description) > 50:
        raise DescriptionError(
            "The description must not exceed 50 characters."
        )

    if not description:
        raise DescriptionError("The description can't be empty string.")


def validate_date(date: str) -> None:
    """
    Validate operation date.

    Args:
        date (str): Operation date.

    Raises:
        DateError: If the date is invalid.
    """
    try:
        datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        raise DateError("The date must be in the format DD-MM-YYYY.")
