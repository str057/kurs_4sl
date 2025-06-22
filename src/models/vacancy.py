from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any


@dataclass
class Salary:
    from_: Optional[int]
    to: Optional[int]
    currency: Optional[str]


@dataclass
class Employer:
    name: str


@dataclass
class Area:
    name: str


@dataclass
class Experience:
    name: str


@dataclass
class Employment:
    name: str


@dataclass
class Snippet:
    requirement: Optional[str]
    responsibility: Optional[str]


@dataclass
class Vacancy:
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
        return self.salary.from_ if self.salary else None

    @property
    def salary_to(self) -> Optional[int]:
        return self.salary.to if self.salary else None

    @property
    def salary_currency(self) -> Optional[str]:
        return self.salary.currency if self.salary else None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_hh_data(cls, data: Dict[str, Any]):
        if not isinstance(data, dict):
            raise ValueError("Vacancy data must be a dictionary")

        if "id" not in data or "name" not in data:
            raise ValueError("Vacancy must have 'id' and 'name' fields")

        # Обработка зарплаты
        salary = None
        if "salary" in data and isinstance(data["salary"], dict):
            salary_data = data["salary"]
            salary = Salary(
                from_=salary_data.get("from"),
                to=salary_data.get("to"),
                currency=salary_data.get("currency"),
            )

        # Обработка работодателя
        employer = None
        if "employer" in data and isinstance(data["employer"], dict):
            employer_data = data["employer"]
            if "name" in employer_data:
                employer = Employer(name=str(employer_data["name"]))

        # Обработка региона
        area = None
        if "area" in data and isinstance(data["area"], dict):
            area_data = data["area"]
            if "name" in area_data:
                area = Area(name=str(area_data["name"]))

        # Обработка опыта
        experience = None
        if "experience" in data and isinstance(data["experience"], dict):
            experience_data = data["experience"]
            if "name" in experience_data:
                experience = Experience(name=str(experience_data["name"]))

        # Обработка занятости
        employment = None
        if "employment" in data and isinstance(data["employment"], dict):
            employment_data = data["employment"]
            if "name" in employment_data:
                employment = Employment(name=str(employment_data["name"]))

        # Обработка сниппета
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
