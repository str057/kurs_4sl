import unittest
import os
import tempfile
from typing import Dict
from src.storage.json_storage import JSONStorage  # Или ваш путь к модулю


class TestJSONStorage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.temp_dir.name, "test_vacancies.json")
        self.storage = JSONStorage(file_path=self.test_file)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_dict_vacancy(self):
        """Тест добавления вакансии в виде словаря"""
        test_vacancy = {
            "id": "123",
            "name": "Test Vacancy",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
        }

        self.storage.add_vacancy(test_vacancy)
        vacancies = self.storage._read_file()
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0]["id"], "123")

    def test_add_object_vacancy(self):
        """Тест добавления вакансии в виде объекта"""

        class MockVacancy:
            def __init__(self, id_, name):
                self.id = id_
                self.name = name

            def to_dict(self) -> Dict:
                return {"id": self.id, "name": self.name}

        vacancy = MockVacancy("456", "Mock Vacancy")
        self.storage.add_vacancy(vacancy)

        vacancies = self.storage._read_file()
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0]["id"], "456")

    def test_add_duplicate_vacancy(self):
        """Тест на добавление дубликата вакансии"""
        test_vacancy = {"id": "123", "name": "Test Vacancy"}
        self.storage.add_vacancy(test_vacancy)
        self.storage.add_vacancy(test_vacancy)
        vacancies = self.storage._read_file()
        self.assertEqual(len(vacancies), 1)

    def test_invalid_vacancy_data(self):
        """Тест на невалидные данные вакансии"""
        with self.assertRaises(ValueError):
            self.storage.add_vacancy("invalid data")  # Строка без метода to_dict()

        with self.assertRaises(ValueError):
            self.storage.add_vacancy({"name": "No ID"})  # Нет обязательного поля id

        with self.assertRaises(ValueError):
            self.storage.add_vacancy(None)  # None вместо вакансии

    def test_read_empty_file(self):
        """Тест чтения пустого файла"""
        vacancies = self.storage._read_file()
        self.assertEqual(vacancies, [])

    def test_write_and_read_file(self):
        """Тест записи и чтения файла"""
        test_data = [{"id": "1", "name": "Vacancy 1"}, {"id": "2", "name": "Vacancy 2"}]

        self.storage._write_file(test_data)
        vacancies = self.storage._read_file()
        self.assertEqual(len(vacancies), 2)
        self.assertEqual(vacancies[0]["name"], "Vacancy 1")
        self.assertEqual(vacancies[1]["name"], "Vacancy 2")


if __name__ == "__main__":
    unittest.main()
