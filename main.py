from src.api.hh_api import HeadHunterAPI
from src.storage.json_storage import JSONStorage
from src.models.vacancy import Vacancy
from src.utils.filters import (
    filter_vacancies,
    get_vacancies_by_salary,
    sort_vacancies,
    get_top_vacancies,
)
import requests


def display_vacancy(vacancy: Vacancy, index: int) -> None:
    """Выводит информацию о вакансии в консоль"""
    # Формируем информацию о зарплате
    salary_info = "Зарплата не указана"
    if vacancy.salary:
        from_ = vacancy.salary_from if vacancy.salary_from is not None else "не указана"
        to = vacancy.salary_to if vacancy.salary_to is not None else "не указана"
        currency = vacancy.salary_currency if vacancy.salary_currency else ""
        salary_info = f"{from_} - {to} {currency}"

    # Выводим основную информацию
    print(f"\n{index}. {vacancy.name}")

    if vacancy.employer:
        print(f"   Работодатель: {vacancy.employer.name}")

    print(f"   {salary_info}")

    if vacancy.area:
        print(f"   Регион: {vacancy.area.name}")

    if vacancy.experience:
        print(f"   Опыт: {vacancy.experience.name}")

    if vacancy.employment:
        print(f"   Занятость: {vacancy.employment.name}")

    if vacancy.alternate_url:
        print(f"   Ссылка: {vacancy.alternate_url}")

    # Выводим требования и обязанности (если есть)
    if vacancy.snippet and vacancy.snippet.requirement:
        print(f"   Требования: {vacancy.snippet.requirement[:150]}...")

    if vacancy.snippet and vacancy.snippet.responsibility:
        print(f"   Обязанности: {vacancy.snippet.responsibility[:150]}...")


def get_user_input() -> tuple:
    """Получает и валидирует ввод пользователя"""
    print("\nПараметры поиска:")
    print("----------------")

    # Получаем поисковый запрос
    search_query = input(
        "Введите поисковый запрос (например: Python разработчик): "
    ).strip()
    if not search_query:
        raise ValueError("Поисковый запрос не может быть пустым")

    # Получаем количество вакансий для отображения
    try:
        top_n = int(input("Сколько вакансий показать? ").strip())
        if top_n <= 0:
            raise ValueError("Количество вакансий должно быть положительным числом")
    except ValueError:
        raise ValueError(
            "Некорректное количество вакансий. Введите целое число больше 0"
        )

    # Получаем ключевые слова для фильтрации
    filter_words = (
        input("Введите ключевые слова для фильтрации (через пробел): ").strip().split()
    )

    # Получаем диапазон зарплат
    salary_range = input(
        "Введите диапазон зарплат (например: 100000 или 100000-150000): "
    ).strip()

    return search_query, top_n, filter_words, salary_range


def process_vacancies(search_query: str) -> list[Vacancy]:
    """Получает и обрабатывает вакансии с API"""
    print("\nПолучение вакансий с HeadHunter...")

    hh_api = HeadHunterAPI()
    vacancies_data = hh_api.get_vacancies(search_query)

    vacancies = []
    for v in vacancies_data:
        try:
            # Пропускаем невалидные данные
            if not isinstance(v, dict):
                continue

            # Создаем объект Vacancy
            vacancy = Vacancy.from_hh_data(v)
            vacancies.append(vacancy)
        except Exception as e:
            print(f"Ошибка при обработке вакансии: {str(e)}")
            continue

    return vacancies


def save_vacancies(vacancies: list[Vacancy]) -> None:
    """Сохраняет вакансии в JSON файл"""
    print("\nСохранение вакансий...")

    storage = JSONStorage()
    saved_count = 0

    for vacancy in vacancies:
        try:
            storage.add_vacancy(vacancy)
            saved_count += 1
        except Exception as e:
            print(f"Ошибка при сохранении вакансии {vacancy.id}: {str(e)}")
            continue

    print(f"Сохранено вакансий: {saved_count}")


def user_interaction():
    """Основная функция взаимодействия с пользователем"""
    print("\nПрограмма для поиска вакансий с HeadHunter.ru")
    print("===========================================")

    try:
        # Получаем параметры поиска от пользователя
        search_query, top_n, filter_words, salary_range = get_user_input()

        # Получаем и обрабатываем вакансии
        vacancies = process_vacancies(search_query)

        # Сохраняем вакансии
        save_vacancies(vacancies)

        # Фильтруем и сортируем вакансии
        print("\nФильтрация вакансий...")
        filtered_vacancies = filter_vacancies(vacancies, filter_words)
        ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
        sorted_vacancies = sort_vacancies(ranged_vacancies)
        top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

        # Выводим результаты
        print("\nРезультаты поиска:")
        print("-----------------")
        print(f"Всего найдено вакансий: {len(vacancies)}")
        print(f"После фильтрации по ключевым словам: {len(filtered_vacancies)}")
        print(f"Соответствует зарплатному диапазону: {len(ranged_vacancies)}")

        # Выводим топ вакансий
        print(f"\nТоп {len(top_vacancies)} вакансий:")
        print("---------------------")

        if not top_vacancies:
            print("Нет вакансий, соответствующих заданным критериям.")
        else:
            for i, vacancy in enumerate(top_vacancies, 1):
                display_vacancy(vacancy, i)

    except ValueError as e:
        print(f"\nОшибка ввода данных: {e}")
    except requests.exceptions.RequestException as e:
        print(f"\nОшибка при подключении к API: {e}")
    except Exception as e:
        print(f"\nПроизошла непредвиденная ошибка: {str(e)}")
    finally:
        print("\nРабота программы завершена.")


if __name__ == "__main__":
    user_interaction()
