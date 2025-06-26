from dataclasses import dataclass, asdict, field
from typing import Optional, Dict, Any


@dataclass
class Salary:
    """Класс для представления информации о зарплате.

    Attributes:
        from_ (Optional[int]): Нижняя граница вилки зарплаты. None если не указана.
        to (Optional[int]): Верхняя граница вилки зарплаты. None если не указана.
        currency (Optional[str]): Валюта зарплаты (например, "RUR"). None если не указана.
    """

    from_: Optional[int] = field(default=None)
    to: Optional[int] = field(default=None)
    currency: Optional[str] = field(default=None)


@dataclass
class Employer:
    """Класс для представления информации о работодателе.

    Attributes:
        name (str): Название компании-работодателя.
    """

    name: str


@dataclass
class Area:
    """Класс для представления географического региона.

    Attributes:
        name (str): Название региона/города.
    """

    name: str


@dataclass
class Experience:
    """Класс для представления требуемого опыта работы.

    Attributes:
        name (str): Уровень опыта (например, "От 1 года").
    """

    name: str


@dataclass
class Employment:
    """Класс для представления типа занятости.

    Attributes:
        name (str): Тип занятости (например, "Полная занятость").
    """

    name: str


@dataclass
class Snippet:
    """Класс для представления описания вакансии и требований.

    Attributes:
        requirement (Optional[str]): Требования к кандидату. None если не указаны.
        responsibility (Optional[str]): Обязанности. None если не указаны.
    """

    requirement: Optional[str] = field(default=None)
    responsibility: Optional[str] = field(default=None)


@dataclass
class Vacancy:
    """Основной класс для представления вакансии.

    Attributes:
        id (str): Уникальный идентификатор вакансии.
        name (str): Название вакансии.
        salary (Optional[Salary]): Информация о зарплате. None если не указана.
        area (Optional[Area]): Регион работы. None если не указан.
        employer (Optional[Employer]): Работодатель. None если не указан.
        experience (Optional[Experience]): Требуемый опыт. None если не указан.
        employment (Optional[Employment]): Тип занятости. None если не указан.
        snippet (Optional[Snippet]): Описание и требования. None если не указано.
        alternate_url (Optional[str]): Ссылка на вакансию. None если не указана.
    """

    id: str
    name: str
    salary: Optional[Salary] = None
    area: Optional[Area] = None
    employer: Optional[Employer] = None
    experience: Optional[Experience] = None
    employment: Optional[Employment] = None
    snippet: Optional[Snippet] = None
    alternate_url: Optional[str] = None

    @property
    def salary_from(self) -> Optional[int]:
        """Возвращает нижнюю границу зарплаты.

        Returns:
            Optional[int]: Значение зарплаты "от" или None если не указано.
        """
        return self.salary.from_ if self.salary else None

    @property
    def salary_to(self) -> Optional[int]:
        """Возвращает верхнюю границу зарплаты.

        Returns:
            Optional[int]: Значение зарплаты "до" или None если не указано.
        """
        return self.salary.to if self.salary else None

    @property
    def salary_currency(self) -> Optional[str]:
        """Возвращает валюту зарплаты.

        Returns:
            Optional[str]: Код валюты или None если не указан.
        """
        return self.salary.currency if self.salary else None

    def to_dict(self) -> Dict[str, Any]:
        """Преобразует объект вакансии в словарь для сериализации.

        Returns:
            Dict[str, Any]: Словарь с данными вакансии.
        """
        return asdict(self)

    @classmethod
    def from_hh_data(cls, data: Dict[str, Any]) -> "Vacancy":
        """Создает объект Vacancy из данных API HeadHunter.

        Args:
            data (Dict[str, Any]): Словарь с данными вакансии от API.

        Returns:
            Vacancy: Объект вакансии.

        Raises:
            ValueError: Если данные не содержат обязательных полей или имеют неверный формат.
        """
        if not isinstance(data, dict):
            raise ValueError("Vacancy data must be a dictionary")

        if "id" not in data or "name" not in data:
            raise ValueError("Vacancy must have 'id' and 'name' fields")

        salary = None
        if "salary" in data and isinstance(data["salary"], dict):
            salary_data = data["salary"]
            salary = Salary(
                from_=salary_data.get("from"),
                to=salary_data.get("to"),
                currency=salary_data.get("currency"),
            )

        employer = None
        if "employer" in data and isinstance(data["employer"], dict):
            employer_data = data["employer"]
            if "name" in employer_data:
                employer = Employer(name=str(employer_data["name"]))

        area = None
        if "area" in data and isinstance(data["area"], dict):
            area_data = data["area"]
            if "name" in area_data:
                area = Area(name=str(area_data["name"]))

        experience = None
        if "experience" in data and isinstance(data["experience"], dict):
            experience_data = data["experience"]
            if "name" in experience_data:
                experience = Experience(name=str(experience_data["name"]))

        employment = None
        if "employment" in data and isinstance(data["employment"], dict):
            employment_data = data["employment"]
            if "name" in employment_data:
                employment = Employment(name=str(employment_data["name"]))

        snippet = None
        if "snippet" in data and isinstance(data["snippet"], dict):
            snippet_data = data["snippet"]
            snippet = Snippet(
                requirement=snippet_data.get("requirement"),
                responsibility=snippet_data.get("responsibility"),
            )

        return cls(
            id=str(data["id"]),
            name=str(data["name"]),
            salary=salary,
            area=area,
            employer=employer,
            experience=experience,
            employment=employment,
            snippet=snippet,
            alternate_url=data.get("alternate_url"),
        )

    def __str__(self) -> str:
        """Возвращает строковое представление вакансии.

        Returns:
            str: Форматированная строка с основной информацией о вакансии.
        """
        salary_info = "Зарплата не указана"
        if self.salary:
            from_ = self.salary_from if self.salary_from is not None else "не указана"
            to = self.salary_to if self.salary_to is not None else "не указана"
            currency = self.salary_currency if self.salary_currency else ""
            salary_info = f"{from_} - {to} {currency}"

        info = [
            f"Вакансия: {self.name}",
            f"Работодатель: {self.employer.name if self.employer else 'не указан'}",
            f"Зарплата: {salary_info}",
            f"Регион: {self.area.name if self.area else 'не указан'}",
            f"Опыт: {self.experience.name if self.experience else 'не указан'}",
            f"Занятость: {self.employment.name if self.employment else 'не указана'}",
        ]

        if self.alternate_url:
            info.append(f"Ссылка: {self.alternate_url}")

        return "\n".join(info)
