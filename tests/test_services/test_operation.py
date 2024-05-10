from tests.test_app import BaseTests

from business_logic.services import (
    get_all_operation_paginate,
    get_operation,
    delete_operation,
    update_operation,
    create_operation,
)
from business_logic.dto import OperationDTO
from business_logic.exceptions import OperationDoesNotExistError


class OperationTests(BaseTests):
    def setUp(self) -> None:
        super().setUp()
        self.dao.create(
            OperationDTO(
                category="income", amount=14, description="description"
            )
        )
        self.dao.create(
            OperationDTO(
                category="income", amount=500, description="description"
            )
        )
        self.dao.create(
            OperationDTO(
                category="expense", amount=23, description="description"
            )
        )
        self.dao.create(
            OperationDTO(
                category="expense", amount=900, description="description"
            )
        )
        self.dao.create(
            OperationDTO(
                category="expense", amount=50, description="description"
            )
        )
        self.dao.create(
            OperationDTO(
                category="income", amount=1400, description="description"
            )
        )

    def test_get_2_operations_successfully(self) -> None:
        result = get_all_operation_paginate(per_page=2, dao=self.dao)

        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], str)
        self.assertIsInstance(result[1], list)
        self.assertEqual(result[2], {"next"})

    def test_get_next_2_operations_successfully(self) -> None:
        result = get_all_operation_paginate(
            per_page=2, page_number=2, dao=self.dao
        )

        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], str)
        self.assertIsInstance(result[1], list)
        self.assertEqual(result[2], {"prev", "next"})

    def test_get_last_2_operations_successfully(self) -> None:
        result = get_all_operation_paginate(
            per_page=2, page_number=3, dao=self.dao
        )

        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], str)
        self.assertIsInstance(result[1], list)
        self.assertEqual(result[2], {"prev"})

    def test_get_2_operations_with_filter_successfully(self) -> None:
        filter = ("category", "income")
        result = get_all_operation_paginate(
            per_page=2, dao=self.dao, filter=filter
        )

        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], str)
        self.assertIsInstance(result[1], list)
        self.assertEqual(result[2], {"next"})

    def test_operations_with_filter_not_exists(self) -> None:
        filter = ("amount", 9823)
        result = get_all_operation_paginate(
            per_page=2, dao=self.dao, filter=filter
        )
        result_text = (
            "\n------------------------------------\n"
            "No operations found.\n\n0 - Back to main menu\n\n-   "
            "1/0   -\n\nEnter the number of the operation you are interested in: "
        )
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], str)
        self.assertIsInstance(result[1], list)
        self.assertEqual(result[2], set())
        self.assertEqual(result[0], result_text)

    def test_get_operation_successfully(self) -> None:
        self.dao.create(
            OperationDTO(
                id="a5d569f8-3d3e-491d-a8b3-04996a89ed52",
                category="income",
                amount=666,
                description="test",
            )
        )
        result = get_operation(
            operation_id="a5d569f8-3d3e-491d-a8b3-04996a89ed52", dao=self.dao
        )

        self.assertIsInstance(result, str)

    def test_get_operation_not_exists(self) -> None:
        with self.assertRaises(OperationDoesNotExistError):
            get_operation(
                operation_id="96395705-58cf-4806-ab40-b6b7c31f0b20",
                dao=self.dao,
            )

    def test_delete_operation_successfully(self) -> None:
        self.dao.create(
            OperationDTO(
                id="a5d569f8-3d3e-491d-a8b3-04996a89ed52",
                category="income",
                amount=666,
                description="test",
            )
        )
        result = delete_operation(
            operation_id="a5d569f8-3d3e-491d-a8b3-04996a89ed52", dao=self.dao
        )
        result_text = "\n=== Operation successfully deleted ===\n"
        self.assertIsInstance(result, str)
        self.assertEqual(result, result_text)

    def test_delete_operation_is_not_exists(self) -> None:
        with self.assertRaises(OperationDoesNotExistError):
            delete_operation(
                operation_id="96395705-58cf-4806-ab40-b6b7c31f0b20",
                dao=self.dao,
            )

    def test_update_operation_successfully(self) -> None:
        self.dao.create(
            OperationDTO(
                id="a5d569f8-3d3e-491d-a8b3-04996a89ed52",
                category="income",
                amount=666,
                description="test",
            )
        )
        new_data = OperationDTO(
            category="expense", amount=333, description="new_test"
        )
        result = update_operation(
            operation_id="a5d569f8-3d3e-491d-a8b3-04996a89ed52",
            data=new_data,
            dao=self.dao,
        )
        result_text = "\n=== Operation successfully updated ===\n"
        self.assertIsInstance(result, str)
        self.assertEqual(result, result_text)

    def test_update_operation_is_not_exists(self) -> None:
        new_data = OperationDTO(
            category="expense", amount=333, description="new_test"
        )
        with self.assertRaises(OperationDoesNotExistError):
            update_operation(
                operation_id="96395705-58cf-4806-ab40-b6b7c31f0b20",
                data=new_data,
                dao=self.dao,
            )

    def create_operation_successfully(self) -> None:
        new_data = OperationDTO(
            category="income", amount=111, description="new_operation"
        )

        result = create_operation(data=new_data, dao=self.dao)

        self.assertIsNone(result)
