from dataclasses import dataclass
from typing import Optional


@dataclass
class Vacancy:
    """Класс для представления вакансии"""
    __slots__ = ('title', 'url', 'salary_from', 'salary_to', 'currency', 'description', 'requirements')

    title: str
    url: str
    salary_from: Optional[int]
    salary_to: Optional[int]
    currency: Optional[str]
    description: str
    requirements: str

    def __post_init__(self):
        self._validate_data()

    def _validate_data(self) -> None:
        """Валидация данных вакансии"""
        if not isinstance(self.title, str):
            raise ValueError("Название должно быть строкой")
        if not self.url.startswith("http"):
            raise ValueError("Некорректный URL")

    def __lt__(self, other) -> bool:
        """Сравнение вакансий по зарплате (<)"""
        if not isinstance(other, Vacancy):
            raise TypeError("Можно сравнивать только вакансии")
        return (self.salary_from or 0) < (other.salary_from or 0)

    def __gt__(self, other) -> bool:
        """Сравнение вакансий по зарплате (>)"""
        if not isinstance(other, Vacancy):
            raise TypeError("Можно сравнивать только вакансии")
        return (self.salary_from or 0) > (other.salary_from or 0)

    @classmethod
    def cast_to_object_list(cls, vacancies_data: list[dict]) -> list['Vacancy']:
        """Преобразование данных API в список объектов Vacancy"""
        vacancies = []
        for vacancy in vacancies_data:
            salary = vacancy.get('salary', {})
            vacancies.append(cls(
                title=vacancy.get('name', ''),
                url=vacancy.get('alternate_url', ''),
                salary_from=salary.get('from'),
                salary_to=salary.get('to'),
                currency=salary.get('currency'),
                description=vacancy.get('description', ''),
                requirements=vacancy.get('snippet', {}).get('requirement', '')
            ))
            return vacancies
