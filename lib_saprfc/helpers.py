from .client import ApiClient
from .process import ProcessQuery


class ReadTable(object):

    def __init__(self, table_name, fields=None, options=None):
        self._table_name = table_name
        self._options = options
        self._fields = fields
        self._api_client = None
        self.data = self.process_data()

    @property
    def api_client(self):
        if not self._api_client:
            self._api_client = ApiClient()
        return self._api_client

    def call_sap(self):
        atribute = {"QUERY_TABLE": self._table_name, 'DELIMITER': "|"}
        if self._options:
            atribute['OPTIONS'] = self._options
        if self._fields:
            atribute['FIELDS'] = self._fields
        result = self.api_client.post("RFC_READ_TABLE", atribute)
        return result.get('DATA')

    def process_data(self):
        data = self.call_sap()
        return ProcessQuery(data)
