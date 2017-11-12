import os
try:
    from sapnwrfc import base as sap_base
except:
    sap_base = None
from .exceptions import DontHaveAttribute, IError
from .process import ProcessError, ProcessStructure


class ApiClient(object):
    """
    This is a Api to connect to sap. It is for reuse to all projects.

    Attributes:
        # Private
            self._config() -> it load the config to connect to sap.
            self._connection = -> It containt the instaces of connection.
    """
    connection = None

    def __new__(cls, *args, **kwargs):
        cls._config()
        cls.connection = cls._connect()
        print("se creo una conneccion")
        return super(ApiClient, cls).__new__(cls, *args, **kwargs)

    @staticmethod
    def _config():
        """
        This load the config to connect to sap.
        It fuction does not return value.
        """
        project_root = os.path.dirname(__file__)
        if sap_base:
            sap_base.config_location = os.path.join(
                project_root, 'conf/sap.dev.yml')
            sap_base.load_config()

    @staticmethod
    def _connect():
        """
        This function create a connection in SAP.

        Return:
            connection
        """
        return sap_base.rfc_connect()

    def _add_parameter(self, function, parameters):
        """ This function add attr to functon.

        Paramter:
            function: The instance of function in sap.
        Return:
            function: With all parameter was set
        """
        for key, value in parameters.items():
            try:
                getattr(function, key)(value)
            except (AttributeError, TypeError):
                raise DontHaveAttribute(
                    'La function {0} no tiene el atributo {1}.'.format(
                        function.name, key))
        return function

    def _discover_function(self, rfc_function):
        """
        This discover a function in SAP.

        Parameter:
            rfc_function str(): The name of function in SAP.
        Return:
            instance of function discover
        """
        return self.connection.discover(rfc_function)

    def get(self, rfc_function, parameters=None):
        """
        This method consult to sap and return the value send sap.

        Parameter:
            rfc_function str(): the name of function in sap.
        Return:
            Value send sap.
        """
        # Discover function in sap
        function_discover = self._discover_function(rfc_function)

        # Create call
        function = function_discover.create_function_call()

        # Set parameters
        if parameters:
            self._add_parameter(function, parameters)

        # Execute Funtion in SAP
        function.invoke()

        # Return Values
        return self.return_value(function)

    def post(self, rfc_function, values):
        """
        This method call a function in sap that insert values.

        Parameters:
            rfc_function str(): -> the function name.

        Return:
            Value send sap.
        """
        # Discover function
        function_discover = self._discover_function(rfc_function)

        # Create call function
        function = function_discover.create_function_call()

        # Set paramters
        self._add_parameter(function, values)

        # Execute Function in sap
        function.invoke()

        # return values
        return self.return_value(function)

    def return_value(self, function):
        """
        This method process the result of consult sap
        and return the final result.

        Parameters:
            function of sap
        Return:
            In case all are great List(dictionary)
            In case are error a exception with errors.
        """
        structure = function.handle.parameters
        if 'I_ERROR' in structure.keys() and \
            isinstance(structure.get('I_ERROR').values, list):
            if structure.get('I_ERROR').values != []:
                process_error = ProcessError(structure.get('I_ERROR').values)
                raise IError(process_error.errors)
        return ProcessStructure(structure).data

    def __del__(self):
        self.connection.close()
        print('Cerrando conexion sap')
