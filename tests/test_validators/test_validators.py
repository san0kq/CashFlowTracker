from tests.test_app import BaseTests

from presentation.validators import (
    validate_amount,
    validate_category,
    validate_date,
    validate_description,
    validate_user_choice,
)
from presentation.exceptions import (
    AmountError,
    CategoryError,
    DateError,
    DescriptionError,
    UserChoiceError,
)


class ValidatorsTests(BaseTests):
    def test_validate_big_amount(self) -> None:
        with self.assertRaises(AmountError):
            validate_amount(amount="5000000")

    def test_validate_negative_amount(self) -> None:
        with self.assertRaises(AmountError):
            validate_amount(amount="-23")

    def test_validate_string_amount(self) -> None:
        with self.assertRaises(AmountError):
            validate_amount(amount="test_string")

    def test_validate_empty_amount(self) -> None:
        with self.assertRaises(AmountError):
            validate_amount(amount="")

    def test_validate_amount_successfully(self) -> None:
        result = validate_amount(amount="50")

        self.assertIsNone(result)

    def test_validate_category_successfully(self) -> None:
        result = validate_category(category="income")

        self.assertIsNone(result)

    def test_validate_category_not_exists(self) -> None:
        with self.assertRaises(CategoryError):
            validate_category(category="test")

    def test_validate_empty_category(self) -> None:
        with self.assertRaises(CategoryError):
            validate_category(category="")

    def test_validate_date_successfully(self) -> None:
        result = validate_date(date="10-11-2024")

        self.assertIsNone(result)

    def test_validate_date_wrong(self) -> None:
        with self.assertRaises(DateError):
            validate_date(date="99-99-2023")

        with self.assertRaises(DateError):
            validate_date(date="-99-2023")

        with self.assertRaises(DateError):
            validate_date(date="01-01-2023 11:12:13")

        with self.assertRaises(DateError):
            validate_date(date="01-01-0000")

        with self.assertRaises(DateError):
            validate_date(date="2024")

        with self.assertRaises(DateError):
            validate_date(date="test")

        with self.assertRaises(DateError):
            validate_date(date="2024-11-11")

        with self.assertRaises(DateError):
            validate_date(date="")

    def test_validate_description_successfully(self) -> None:
        result = validate_description(description="test")

        self.assertIsNone(result)

    def test_validate_big_description(self) -> None:
        with self.assertRaises(DescriptionError):
            validate_description(
                "testtesttesttesttesttesttesttesttesttest"
                "testtesttesttesttesttesttesttesttesttest"
            )

    def test_validate_empty_description(self) -> None:
        with self.assertRaises(DescriptionError):
            validate_description("")

    def test_user_choice_successfully(self) -> None:
        result = validate_user_choice(choice="5", max_choice=10)

        self.assertIsNone(result)

    def test_user_big_choice(self) -> None:
        with self.assertRaises(UserChoiceError):
            validate_user_choice("10", max_choice=5)

    def test_user_negative_choice(self) -> None:
        with self.assertRaises(UserChoiceError):
            validate_user_choice("-2", max_choice=10)

    def test_user_empty_choice(self) -> None:
        with self.assertRaises(UserChoiceError):
            validate_user_choice("", max_choice=10)

    def test_user_string_choice(self) -> None:
        with self.assertRaises(UserChoiceError):
            validate_user_choice("next", max_choice=10)

    def test_user_wrong_button_choice(self) -> None:
        with self.assertRaises(UserChoiceError):
            validate_user_choice("prev", max_choice=10, buttons={"next"})

    def test_user_button_choice_successfully(self) -> None:
        result = validate_user_choice(
            "prev", max_choice=10, buttons={"next", "prev"}
        )

        self.assertIsNone(result)
