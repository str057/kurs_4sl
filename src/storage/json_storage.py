import json
import os
from typing import List, Dict, Union


class JSONStorage:
    def __init__(self, file_path: str = "data/vacancies.json"):
        self.file_path = file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    def add_vacancy(self, vacancy: Union[Dict, object]) -> None:
        """Добавляет вакансию в хранилище"""
        try:
            vacancy_dict = self._convert_to_dict(vacancy)
            self._validate_vacancy(vacancy_dict)

            vacancies = self._read_file()
            if not self._vacancy_exists(vacancies, vacancy_dict):
                vacancies.append(vacancy_dict)
                self._write_file(vacancies)
        except (ValueError, AttributeError) as e:
            raise ValueError(f"Invalid vacancy data: {str(e)}")

    def _convert_to_dict(self, vacancy: Union[Dict, object]) -> Dict:
        """Конвертирует объект вакансии в словарь"""
        if isinstance(vacancy, dict):
            return vacancy
        elif hasattr(vacancy, "to_dict") and callable(vacancy.to_dict):
            return vacancy.to_dict()
        else:
            raise AttributeError(
                "Vacancy must be a dictionary or have to_dict() method"
            )

    def _validate_vacancy(self, vacancy: Dict) -> None:
        """Проверяет валидность данных вакансии"""
        if not isinstance(vacancy, dict):
            raise ValueError("Vacancy data must be a dictionary")
        if "id" not in vacancy or not isinstance(vacancy["id"], str):
            raise ValueError("Vacancy must have a string 'id' field")

    def _vacancy_exists(self, vacancies: List[Dict], new_vacancy: Dict) -> bool:
        """Проверяет, существует ли уже такая вакансия"""
        return any(v.get("id") == new_vacancy.get("id") for v in vacancies)

    def _read_file(self) -> List[Dict]:
        """Читает вакансии из файла"""
        if not os.path.exists(self.file_path):
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_file(self, vacancies: List[Dict]) -> None:
        """Записывает вакансии в файл"""
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)
