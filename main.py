from src.api.hh_api import HeadHunterAPI
from src.storage.json_storage import JSONStorage
from src.models.vacancy import Vacancy
from src.utils.filters import (
    filter_vacancies,
    get_vacancies_by_salary,
    sort_vacancies,
    get_top_vacancies
)


def user_interaction():
    """Основная функция взаимодействия с пользователем"""
    print("Программа для поиска вакансий с HeadHunter.ru")
    print("-------------------------------------------")

    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Сколько вакансий показать? "))
    filter_words = input("Введите ключевые слова для фильтрации (через пробел): ").split()
    salary_range = input("Введите диапазон зарплат (например: 100000-1500000): ")

    # Получение вакансий
    hh_api = HeadHunterAPI()
    vacancies_data = hh_api.get_vacancies(search_query)
    vacancies = Vacancy.cast_to_object_list(vacancies_data)

    # Сохранение
    storage = JSONStorage()
    for vacancy in vacancies:
        storage.add_vacancy(vacancy)

    # Фильтрация и сортировка
    filtered = filter_vacancies(vacancies, filter_words)
    ranged = get_vacancies_by_salary(filtered, salary_range)
    sorted_vac = sort_vacancies(ranged)
    top_vacancies = get_top_vacancies(sorted_vac, top_n)

    # Вывод результатов
    print("\nНайденные вакансии:")
    for i, vacancy in enumerate(top_vacancies, 1):
        salary = f"{vacancy.salary_from or '?'}-{vacancy.salary_to or '?'} {vacancy.currency or ''}"
        print(f"\n{i}. {vacancy.title}")
        print(f"   Зарплата: {salary}")
        print(f"   Ссылка: {vacancy.url}")
        print(f"   Требования: {vacancy.requirements[:100]}...")

    print("\nПоиск завершен. Данные сохранены в data/vacancies.json")


if __name__ == "__main__":
    user_interaction()