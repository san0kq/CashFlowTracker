from __future__ import annotations

import json
from uuid import uuid4
from datetime import datetime
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from uuid import UUID

from business_logic.dto import OperationDTO
from data_access.exceptions import RecordDoesNotExistError


def db_provider(data_name: str, data_type: str) -> "DBJsonDAO":
    """
    Provide a database provider based on the specified data type.

    Args:
        data_name (str): The name of the data.
        data_type (str): The type of the data.

    Returns:
        DBJsonDAO: A database provider instance.
    """
    return DBJsonDAO(data_name=data_name, data_type=data_type)


class FileDB:
    def __init__(self, data_name: str, data_type: str) -> None:
        self._data_name = data_name
        self._data_type = data_type
        self._database = self._data_name + self._data_type


class DBJsonDAO(FileDB):
    def read(
        self,
        operation_id: Optional[UUID] = None,
        filter: Optional[tuple[str, str | float | datetime]] = None,
    ) -> dict[UUID, dict[str, str | float]] | OperationDTO | None:
        """
        Read data from the JSON database.

        Args:
            operation_id (Optional[UUID]): The ID of the operation to read.
            filter (Optional[tuple[str, str | float | datetime]]): A filter for the data.

        Returns:
            Union[dict[UUID, dict[str, str | float]], OperationDTO, None]: The read data.
        """
        with open(self._database, "r") as file:
            json_data: dict[UUID, dict[str, str | float]] = json.load(file)

            if filter:
                filtered_data = {}
                key = filter[0]
                value = filter[1]

                if key == "date":
                    for operation_uuid in json_data:
                        data_date = datetime.strptime(
                            json_data[operation_uuid][key],
                            "%Y-%m-%dT%H:%M:%S.%f",
                        )
                        if (
                            data_date.year == value.year
                            and data_date.month == value.month
                            and data_date.day == value.day
                        ):
                            filtered_data[operation_uuid] = json_data[
                                operation_uuid
                            ]

                else:
                    for operation_uuid in json_data:
                        if json_data[operation_uuid][key] == value:
                            filtered_data[operation_uuid] = json_data[
                                operation_uuid
                            ]

                return filtered_data

            elif not operation_id:
                return json_data

            elif operation := json_data.get(operation_id):
                return OperationDTO(
                    category=operation.get("category"),
                    amount=operation.get("amount"),
                    description=operation.get("description"),
                    date=datetime.strptime(
                        operation.get("date"), "%Y-%m-%dT%H:%M:%S.%f"
                    ),
                    id=operation_id,
                )
            else:
                raise RecordDoesNotExistError("Record does not exist.")

    def create(self, data: OperationDTO) -> None:
        """
        Create a new operation in the JSON database.

        Args:
            data (OperationDTO): The operation data.
        """
        with open(self._database, "r") as file:
            json_data: dict[UUID, dict[str, str | float]] = json.load(file)

            operation: dict[str, datetime | str | float] = {
                "date": datetime.now().isoformat(),
                "category": data.category,
                "amount": data.amount,
                "description": data.description,
            }

            if not data.id:
                new_id: str = str(uuid4())
                while new_id in json_data:
                    new_id = str(uuid4())
            else:
                new_id = data.id

            json_data[new_id] = operation

        with open(self._database, "w") as file:
            json.dump(json_data, file, indent=2)

    def update(self, operation_id: UUID, data: OperationDTO) -> None:
        """
        Update an operation in the JSON database.

        Args:
            operation_id (UUID): The ID of the operation to update.
            data (OperationDTO): The updated operation data.
        """
        with open(self._database, "r") as file:
            json_data: dict[UUID, dict[str, str | float]] = json.load(file)

            if old_data := json_data.get(operation_id):
                json_data[operation_id] = {
                    "date": old_data["date"],
                    "category": (
                        data.category
                        if data.category
                        else old_data["category"]
                    ),
                    "amount": (
                        data.amount if data.amount else old_data["amount"]
                    ),
                    "description": (
                        data.description
                        if data.description
                        else old_data["description"]
                    ),
                }
            else:
                raise RecordDoesNotExistError("Record does not exist.")
        with open(self._database, "w") as file:
            json.dump(json_data, file, indent=2)

    def delete(self, operation_id: UUID) -> None:
        """
        Delete an operation from the JSON database.

        Args:
            operation_id (UUID): The ID of the operation to delete.
        """
        with open(self._database, "r") as file:
            json_data: dict[UUID, dict[str, str | float]] = json.load(file)
            if json_data.get(operation_id):
                json_data.pop(operation_id)
            else:
                raise RecordDoesNotExistError("Record does not exist.")
        with open(self._database, "w") as file:
            json.dump(json_data, file, indent=2)
