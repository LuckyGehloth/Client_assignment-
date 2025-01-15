# Unit Tests
from main import app
import unittest
from unittest.mock import patch

class TestMovieAPI(unittest.TestCase):
    @patch("requests.get")
    def test_get_movies_success(self, mock_get):
        mock_discover_response = {
            "results": [
                {
                    "id": 1,
                    "title": "Test Movie",
                    "release_date": "2019-01-01",
                    "vote_average": 8.5
                }
            ]
        }

        mock_credits_response = {
            "crew": [
                {"name": "Editor One", "known_for_department": "Editing"},
                {"name": "Editor Two", "known_for_department": "Editing"}
            ]
        }

        def mock_requests_get(url, *args, **kwargs):
            if "discover" in url:
                mock_response = unittest.mock.Mock()
                mock_response.json.return_value = mock_discover_response
                return mock_response
            elif "credits" in url:
                mock_response = unittest.mock.Mock()
                mock_response.json.return_value = mock_credits_response
                return mock_response

        mock_get.side_effect = mock_requests_get

        with app.test_client() as client:
            response = client.get("/movies?year=2019")
            data = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["title"], "Test Movie")
            self.assertEqual(data[0]["editors"], ["Editor One", "Editor Two"])

    def test_invalid_year(self):
        with app.test_client() as client:
            response = client.get("/movies?year=19")
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid year format", response.get_json()["error"])

if __name__ == "_main_":
    unittest.main()
