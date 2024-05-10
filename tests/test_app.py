import unittest
from os import remove
import json

from data_access.dao import db_provider


class BaseTests(unittest.TestCase):
    def setUp(self) -> None:
        with open("test_db.json", "w") as file:
            json.dump({}, file)

        self.dao = db_provider(data_name="test_db", data_type=".json")

    def tearDown(self) -> None:
        remove("test_db.json")


if __name__ == "__main__":
    unittest.main()
