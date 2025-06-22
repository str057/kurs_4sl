import unittest
from unittest.mock import patch, MagicMock
from src.api.hh_api import HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):
    def setUp(self):
        self.api = HeadHunterAPI()

    @patch("requests.get")
    def test_connect_to_api_success(self, mock_get):
        """Тест успешного подключения к API"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Не должно быть исключения
        self.api._connect_to_api()

    @patch("requests.get")
    def test_connect_to_api_failure(self, mock_get):
        """Тест неудачного подключения к API"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(ConnectionError):
            self.api._connect_to_api()

    @patch("requests.get")
    def test_get_vacancies_success(self, mock_get):
        """Тест успешного получения вакансий"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {"id": "1", "name": "Python Developer"},
                {"id": "2", "name": "Java Developer"},
            ]
        }
        mock_get.return_value = mock_response

        vacancies = self.api.get_vacancies("developer")
        self.assertEqual(len(vacancies), 2)
        self.assertEqual(vacancies[0]["name"], "Python Developer")

    @patch("requests.get")
    def test_get_vacancies_empty(self, mock_get):
        """Тест получения пустого списка вакансий"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        vacancies = self.api.get_vacancies("nonexistent")
        self.assertEqual(len(vacancies), 0)

    @patch("requests.get")
    def test_get_vacancies_params(self, mock_get):
        """Тест передачи параметров в запрос"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        self.api.get_vacancies("python", per_page=50)

        # Проверяем переданные параметры
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(kwargs["params"]["text"], "python")
        self.assertEqual(kwargs["params"]["per_page"], 50)
        self.assertEqual(kwargs["params"]["area"], 113)

    @patch("requests.get")
    def test_get_vacancies_error(self, mock_get):
        """Тест обработки ошибки запроса"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_get.return_value = mock_response

        with self.assertRaises(Exception):
            self.api.get_vacancies("python")


if __name__ == "__main__":
    unittest.main()
