import json
import os
from typing import List, Dict, Optional
from src.models.vacancy import Vacancy
from src.storage.abstract_storage import AbstractStorage


class JSONStorage(AbstractStorage):
    """Класс для работы с JSON-хранилищем вакансий"""

    def __init__(self, filename: str = "data/vacancies.json"):
        self.__filename = filename
        self._ensure_directory_exists()

        if not os.path.exists(self.__filename):
            with open(self.__filename, 'w') as file:
                json.dump([], file)

    def _ensure_directory_exists(self) -> None:
        """Создает директорию, если она не существует"""
        os.makedirs(os.path.dirname(self.__filename), exist_ok=True)

    def __read_file(self) -> List[Dict]:
        """Чтение данных из файла"""
        with open(self.__filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # Возвращаем список вакансий из ключа 'items'
            return data.get("items", [])

    def __write_file(self, data: List[Dict]) -> None:
        """Запись данных в файл"""
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump({"items": data}, file, indent=2, ensure_ascii=False)  # Записываем с ключом 'items'

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии в хранилище"""
        vacancies = self.__read_file()

        # Убедитесь, что vacancies - это список
        if not isinstance(vacancies, list):
            raise ValueError("Ожидался список вакансий, но получено: {}".format(type(vacancies)))

        # Проверяем, что в vacancies находятся словари
        if not all(isinstance(v, dict) for v in vacancies):
            raise ValueError("Ожидался список словарей, но получено: {}".format(vacancies))

        if not any(v['url'] == vacancy.url for v in vacancies):
            vacancies.append({
                'title': vacancy.title,
                'url': vacancy.url,
                'salary_from': vacancy.salary_from,
                'salary_to': vacancy.salary_to,
                'currency': vacancy.currency,
                'description': vacancy.description,
                'requirements': vacancy.requirements
            })
            self.__write_file({"items": vacancies})  # Записываем обратно в формате с ключом 'items'

    def get_vacancies(self, criteria: Optional[Dict] = None) -> List[Vacancy]:
        """Получение вакансий по критериям"""
        vacancies_data = self.__read_file()
        vacancies = []

        for vacancy_data in vacancies_data:
            vacancy = Vacancy(
                title=vacancy_data['title'],
                url=vacancy_data['url'],
                salary_from=vacancy_data['salary_from'],
                salary_to=vacancy_data['salary_to'],
                currency=vacancy_data['currency'],
                description=vacancy_data['description'],
                requirements=vacancy_data['requirements']
            )

            if not criteria or all(
                    getattr(vacancy, key) == value
                    for key, value in criteria.items()
            ):
                vacancies.append(vacancy)

        return vacancies

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаление вакансии из хранилища"""
        vacancies = self.__read_file()
        vacancies = [v for v in vacancies if v['url'] != vacancy.url]
        self.__write_file(vacancies)