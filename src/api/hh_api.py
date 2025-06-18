import requests
from typing import List, Dict
from src.api.abstract_api import AbstractAPI


class HeadHunterAPI(AbstractAPI):
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self.__base_url = "https://api.hh.ru/vacancies"
        self._connect_to_api()

    def _connect_to_api(self) -> None:
        """Подключение к API HH.ru"""
        response = requests.get(self.__base_url)
        if response.status_code != 200:
            raise ConnectionError(f"Ошибка подключения к API HH. Код: {response.status_code}")

    def get_vacancies(self, search_query: str, per_page: int = 100) -> List[Dict]:
        """Получение вакансий с HH.ru"""
        params = {
            "text": search_query,
            "per_page": per_page,
            "area": 113,  # Россия
            "only_with_salary": True
        }

        response = requests.get(self.__base_url, params=params)
        response.raise_for_status()

        # Возвращаем только 'items'
        return response.json().get("items", [])