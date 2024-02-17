import unittest
from unittest.mock import patch, MagicMock
from app.api.core.handler import ApiHandler


class TestApiHandler(unittest.TestCase):
    @patch('app.api.core.component.consult_access_componet.ConsultAccessComponent.all_info_run')
    def test_list_all_handler(self, mock_all_info_run):
        mock_response = {'access_points': [], 'pagination_info': {}}
        mock_all_info_run.return_value = mock_response
        result = ApiHandler.list_all_handler(offset=0, limit=10)
        self.assertEqual(result, mock_response)

    @patch('app.api.core.component.consult_access_componet.ConsultAccessComponent.by_id_run')
    def test_data_by_id_handler(self, mock_by_id_run):
        mock_response = {'id': '123', 'name': 'Test AP'}
        mock_by_id_run.return_value = mock_response
        result = ApiHandler.data_by_id_handler(id='123')
        self.assertEqual(result, mock_response)

    @patch('app.api.core.component.consult_access_componet.ConsultAccessComponent.by_colony_run')
    def test_data_by_colony_handler(self, mock_by_colony_run):
        mock_response = {'access_points': [], 'pagination_info': {}}
        mock_by_colony_run.return_value = mock_response
        result = ApiHandler.data_by_colony_handler(colony='Test Colony', offset=0, limit=10)
        self.assertEqual(result, mock_response)

    @patch('app.api.core.component.consult_access_componet.ConsultAccessComponent.proximity_run')
    def test_wifi_ordered_by_proximity_handler(self, mock_proximity_run):
        mock_response = {'access_points': [], 'pagination_info': {}}
        mock_proximity_run.return_value = mock_response
        result = ApiHandler.wifi_ordered_by_proximity_handler(latitude=0.0, longitude=0.0, offset=0, limit=10)
        self.assertEqual(result, mock_response)

    def run_test(self):
        unittest.main()
