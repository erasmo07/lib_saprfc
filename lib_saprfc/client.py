import sys
import os
try:
    from sapnwrfc import base as sap_base
except:
    pass


class ApiClient(object):
    """
    This is a Api to connect to sap. It is for reuse to all projects.

    Attributes:
        # Private
            self._config() -> it load the config to connect to sap.
            self._connection = -> It containt the instaces of connection.
    """

    def __init__(self):
        self._config()
        self._connection = None
        self._connect()

    def _config(self):
        """
        This load the config to connect to sap.
        It fuction does not return value.
        """
        project_root = os.path.dirname(__file__)
        sap_base.config_location = os.path.join(
            project_root, 'conf/sap.dev.yml')
        sap_base.load_config()

    def _connect(self):
        """
        This function create a connection in SAP.

        Return:
            connection
        """
        try:
            if not self._connection:
                self._connection = sap_base.rfc_connect()
            return self._connection
        except Exception as error:
            print error
            sys.exit(1)

    def _add_paramter(self, function, **parameters):
        """ This function add attr to functon.

        Paramter:
            function: The instance of function in sap.
        Return:
            function: With all parameter was set
        """
        for key, value in parameters.items():
            if hasattr(function, key):
                getattr(function, key)(value)
        return function

    def _discover_function(self, rfc_function):
        """
        This discover a function in SAP.

        Parameter:
            rfc_function str(): The name of function in SAP.
        Return:
            instance of function discover
        """
        return self._connection.discover(rfc_function)

    def get(self, rfc_function, parameters=None):
        """
        This method consult to sap and return the value send sap.

        Parameter:
            rfc_function str(): the name of function in sap.
        Return:
            Value send sap.
        """
        try:
            # Discover function in sap
            function_discover = self._discover_function(rfc_function)

            # Create call
            function = function_discover.create_function_call()

            # Set parameters
            if parameters:
                self._add_paramter(function, **parameters)

            # Execute Funtion in SAP
            function.invoke()
            return function.DATA.value
        except Exception as error:
            print error
            sys.exit(1)

    def __del__(self):
        print 'Cerrando conexion sap'
        self._connection.close()
