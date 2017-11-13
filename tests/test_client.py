"""
This module contains all the tests related to the client file.

- Objective
    The idea of this module is to fully test relate with the client file,
    every element of that file must have a test in this place.
"""
from unittest import TestCase
from mock import patch, MagicMock
from lib_saprfc.client import ApiClient


class TestApiClient(TestCase):
    """
    This test class test all behavior of class ApiClient.
    """

    @patch('lib_saprfc.client.sap_base')
    def test_static_method_config(self, mock_sap_base):
        """
        This test the behavior of staticmethod _config.
        """
        # Value to send
        cls = ApiClient

        # Mock
        sap_base = MagicMock()
        sap_base.config_location = None
        sap_base.load_config.return_value = None
        mock_sap_base.return_value = sap_base

        # Action
        cls._config()

        # Validation
        mock_sap_base.load_config.assert_called()
        self.assertIsNotNone(mock_sap_base.config_locationn)
        self.assertIsInstance(mock_sap_base.config_location, str)

    @patch('lib_saprfc.client.sap_base')
    def test_flow_get_method(self, mock_sap_base):
        # Value to send
        rfc_function = 'TEST'

        # Mock
        function = MagicMock()
        function.invoke.return_value = None

        function_discover = MagicMock()
        function_discover.create_function_call.return_value = function

        connection = MagicMock()
        connection.discover.return_value = function_discover

        mock_sap_base.rfc_connect.return_value = connection

        # Action
        cls = ApiClient()
        result = cls.get(rfc_function)

        # Validation
        function.invoke.assert_called()
        function_discover.create_function_call.assert_called()
        connection.discover.assert_called()
        mock_sap_base.rfc_connect.assert_called()
        self.assertEqual(result, {})
