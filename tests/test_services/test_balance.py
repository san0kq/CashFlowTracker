from tests.test_app import BaseTests

from business_logic.services import get_balance
from business_logic.dto import OperationDTO


class BalanceTests(BaseTests):
    def test_get_positive_balance_successfully(self) -> None:
        self.dao.create(
            OperationDTO(
                category="income", amount=100, description="description"
            )
        )
        self.dao.create(
            OperationDTO(
                category="income", amount=500, description="description"
            )
        )
        self.dao.create(
            OperationDTO(
                category="expense", amount=300, description="description"
            )
        )
        self.dao.create(
            OperationDTO(
                category="expense", amount=10, description="description"
            )
        )
        result = get_balance(dao=self.dao)

        self.assertIsInstance(result, float)
        self.assertEqual(result, 290.0)

    def test_get_negative_balance_successfully(self) -> None:
        self.dao.create(
            OperationDTO(
                category="income", amount=100, description="description"
            )
        )
        self.dao.create(
            OperationDTO(
                category="income", amount=500, description="description"
            )
        )
        self.dao.create(
            OperationDTO(
                category="expense", amount=1300, description="description"
            )
        )

        result = get_balance(dao=self.dao)

        self.assertIsInstance(result, float)
        self.assertEqual(result, -700.0)

    def test_get_no_balance(self) -> None:
        result = get_balance(dao=self.dao)

        self.assertIsInstance(result, float)
        self.assertEqual(result, 0.0)
