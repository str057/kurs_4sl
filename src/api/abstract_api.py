from abc import ABC, abstractmethod


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API вакансий"""

    @abstractmethod
    def _connect_to_api(self) -> None:
        """Подключение к API"""
        pass

    @abstractmethod
    def get_vacancies(self, search_query: str, per_page: int = 100) -> list[dict]:
        """Получение вакансий по поисковому запросу"""
        pass
