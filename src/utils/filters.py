from typing import List
from src.models.vacancy import Vacancy


def filter_vacancies(vacancies: List[Vacancy], filter_words: List[str]) -> List[Vacancy]:
    """Фильтрация вакансий по ключевым словам"""
    if not filter_words:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        text = f"{vacancy.description} {vacancy.requirements}".lower()
        if any(word.lower() in text for word in filter_words):
            filtered.append(vacancy)

    return filtered


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """Фильтрация вакансий по диапазону зарплат"""
    if not salary_range:
        return vacancies

    try:
        min_salary, max_salary = map(int, salary_range.split('-'))
    except ValueError:
        return vacancies

    return [
        v for v in vacancies
        if (v.salary_from and v.salary_from >= min_salary and
            v.salary_to and v.salary_to <= max_salary)
    ]

def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
        """Сортировка вакансий по зарплате (по убыванию)"""
        return sorted(vacancies, reverse=True)

def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
        """Получение топ N вакансий"""
        return vacancies[:top_n]