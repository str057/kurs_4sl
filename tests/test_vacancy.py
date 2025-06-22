import unittest
from src.models.vacancy import (
    Vacancy,
    Salary,
    Employer,
    Area,
    Experience,
    Employment,
    Snippet,
)


class TestVacancy(unittest.TestCase):
    def setUp(self):
        # Создаем тестовые данные
        self.sample_data = {
            "id": "123456",
            "name": "Python Developer",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "employer": {"name": "Test Company"},
            "area": {"name": "Moscow"},
            "experience": {"name": "От 1 года до 3 лет"},
            "employment": {"name": "Полная занятость"},
            "snippet": {
                "requirement": "Опыт работы с Python",
                "responsibility": "Разработка новых функций",
            },
            "alternate_url": "https://hh.ru/vacancy/123456",
        }

    def test_create_vacancy_from_dict(self):
        """Тест создания вакансии из словаря"""
        vacancy = Vacancy.from_hh_data(self.sample_data)

        self.assertEqual(vacancy.id, "123456")
        self.assertEqual(vacancy.name, "Python Developer")
        self.assertEqual(vacancy.alternate_url, "https://hh.ru/vacancy/123456")

    def test_salary_properties(self):
        """Тест свойств salary"""
        vacancy = Vacancy.from_hh_data(self.sample_data)

        self.assertEqual(vacancy.salary_from, 100000)
        self.assertEqual(vacancy.salary_to, 150000)
        self.assertEqual(vacancy.salary_currency, "RUR")

    def test_optional_fields(self):
        """Тест необязательных полей"""
        minimal_data = {"id": "789", "name": "Minimal Vacancy"}

        vacancy = Vacancy.from_hh_data(minimal_data)

        self.assertEqual(vacancy.id, "789")
        self.assertEqual(vacancy.name, "Minimal Vacancy")
        self.assertIsNone(vacancy.salary)
        self.assertIsNone(vacancy.employer)
        self.assertIsNone(vacancy.area)

    def test_to_dict_method(self):
        """Тест метода to_dict()"""
        vacancy = Vacancy.from_hh_data(self.sample_data)
        vacancy_dict = vacancy.to_dict()

        self.assertIsInstance(vacancy_dict, dict)
        self.assertEqual(vacancy_dict["id"], "123456")
        self.assertEqual(vacancy_dict["name"], "Python Developer")
        # Исправлено: используем from_ вместо from
        self.assertEqual(vacancy_dict["salary"]["from_"], 100000)

    def test_invalid_data(self):
        """Тест обработки невалидных данных"""
        with self.assertRaises((ValueError, AttributeError)):
            Vacancy.from_hh_data("not a dict")

        with self.assertRaises(ValueError):
            Vacancy.from_hh_data({"invalid": "data"})

    def test_nested_objects(self):
        """Тест вложенных объектов"""
        vacancy = Vacancy.from_hh_data(self.sample_data)

        self.assertIsInstance(vacancy.salary, Salary)
        self.assertEqual(vacancy.salary.from_, 100000)

        self.assertIsInstance(vacancy.employer, Employer)
        self.assertEqual(vacancy.employer.name, "Test Company")

        self.assertIsInstance(vacancy.area, Area)
        self.assertEqual(vacancy.area.name, "Moscow")


if __name__ == "__main__":
    unittest.main()
