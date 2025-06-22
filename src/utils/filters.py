from typing import List
from src.models.vacancy import Vacancy


def filter_vacancies(
    vacancies: List[Vacancy], filter_words: List[str]
) -> List[Vacancy]:
    """Фильтрация вакансий по ключевым словам"""
    if not filter_words:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        vacancy_text = f"{vacancy.name} {vacancy.snippet.requirement or ''} {vacancy.snippet.responsibility or ''}".lower()
        if all(word.lower() in vacancy_text for word in filter_words):
            filtered.append(vacancy)
    return filtered


def get_vacancies_by_salary(
    vacancies: List[Vacancy], salary_range: str
) -> List[Vacancy]:
    """Фильтрация вакансий по диапазону зарплат"""
    if not salary_range.strip():
        return vacancies

    try:
        if salary_range.startswith("-"):
            # Формат "-150000" - максимальная зарплата (проверяем salary_to <= MAX)
            max_salary = int(salary_range[1:])
            min_salary = 0
            check_type = "max"
        elif "-" in salary_range:
            # Формат "100000-150000" - полный диапазон (должны полностью попадать)
            min_salary, max_salary = map(int, salary_range.split("-"))
            check_type = "range"
        else:
            # Формат "140000" - минимальная зарплата (проверяем salary_from >= MIN)
            min_salary = int(salary_range)
            max_salary = float("inf")
            check_type = "min"
    except ValueError:
        print(
            "Некорректный формат зарплаты. Используйте формат: 100000 или 100000-150000"
        )
        return vacancies

    filtered = []
    for v in vacancies:
        if not v.salary:
            continue

        salary_from = v.salary.from_ or 0
        salary_to = v.salary.to or float("inf")

        if check_type == "max":
            # Для "-MAX" - проверяем конечную зарплату <= MAX
            if salary_to <= max_salary:
                filtered.append(v)
        elif check_type == "min":
            # Для "MIN" - проверяем начальную зарплату >= MIN
            if salary_from >= min_salary:
                filtered.append(v)
        else:
            # Для "MIN-MAX" - проверяем полное вхождение диапазона
            if salary_from >= min_salary and salary_to <= max_salary:
                filtered.append(v)
    return filtered


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Сортировка вакансий по зарплате (по убыванию)"""
    return sorted(
        vacancies, key=lambda v: (v.salary_from or 0, v.salary_to or 0), reverse=True
    )


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """Получение топ N вакансий"""
    return vacancies[:top_n] if top_n > 0 else []
