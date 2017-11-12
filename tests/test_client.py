"""
This module contains all the tests related to the client file.

- Objective
    The idea of this module is to fully test relate with the client file,
    every element of that file must have a test in this place.
"""
import os
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

        # Expect value
        path = '/Users/mazy/Documents/Projects/lib_saprfc/lib_saprfc/conf/sap.dev.yml'

        # Mock
        sap_base = MagicMock()
        sap_base.config_location = None
        sap_base.load_config.return_value = None
        mock_sap_base.return_value = sap_base

        # Action
        cls._config()

        # Validation
        mock_sap_base.load_config.assert_called()
        self.assertEqual(mock_sap_base.config_location, path)
