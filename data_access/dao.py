from __future__ import annotations

import json
from uuid import uuid4
from datetime import datetime
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from uuid import UUID

from business_logic.dto import OperationDTO
from data_access.exceptions import RecordDoesNotExistError


def db_provider(
        data_name: str,
        data_type: str
    ) -> 'DBJsonDAO':
    if data_type == '.json':
        return DBJsonDAO(data_name=data_name, data_type=data_type)


class FileDB:
    def __init__(self, data_name: str, data_type: str) -> None:
        self.data_name = data_name
        self.data_type = data_type
        self.database = self.data_name + self.data_type


class DBJsonDAO(FileDB):
    def read(self, operation_id: UUID = None) -> Optional[dict[str, dict[str, str | float | datetime]] | OperationDTO]:
        with open(self.database, 'r') as file:
            json_data = json.load(file)
            
            if not operation_id:
                return json_data

            if operation := json_data.get(operation_id):
                return OperationDTO(
                    category=operation.get('category'),
                    amount=operation.get('amount'),
                    description=operation.get('description'),
                    date=datetime.strptime(operation.get('date'), '%Y-%m-%dT%H:%M:%S.%f'),
                    id=operation_id
                )
            else:
                raise RecordDoesNotExistError(
                    'Record does not exist.'
                )

    def create(self, data: OperationDTO) -> None:
        with open(self.database, 'r') as file:
            json_data = json.load(file)

            operation = {
                'date': datetime.now().isoformat(),
                'category': data.category,
                'amount': data.amount,
                'description': data.description,
            }

            new_id = str(uuid4())
            while new_id in json_data:
                new_id = str(uuid4())

            json_data[str(uuid4())] = operation

        with open(self.database, 'w') as file:
            json.dump(json_data, file, indent=2)

    def update(
            self,
            operation_id: UUID,
            data: OperationDTO) -> None:

        with open(self.database, 'r') as file:
            json_data = json.load(file)

            if old_data := json_data.get(operation_id):
                json_data[operation_id] = {
                    'date': old_data['date'],
                    'category': data.category if data.category else old_data['category'],
                    'amount': data.amount if data.amount else old_data['amount'],
                    'description': data.description if data.description else old_data['description'],
                }
            else:
                raise RecordDoesNotExistError(
                    'Record does not exist.'
                )
        with open(self.database, 'w') as file:
            json.dump(json_data, file, indent=2)

    def delete(self, operation_id: UUID) -> None:
        with open(self.database, 'r') as file:
            json_data = json.load(file)
            if json_data.get(operation_id):
                json_data.pop(operation_id)
            else:
                raise RecordDoesNotExistError(
                    'Record does not exist.'
                )
        with open(self.database, 'w') as file:
            json.dump(json_data, file, indent=2)

    def truncate(self) -> str:
        with open(self.database, 'w') as file:
            return f'All records from the "{file.name}" have been deleted.'
