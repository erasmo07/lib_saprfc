"""
This contait all class about to process data obtain to sap.
    The class ProcessQuery
        - It take the data obtaint of sap and proces that
          and put in data attribute.

        Description of methods:
            1 - process_data -> It process the query of sap
                and convert in a list of dictionary.
                Ex. [{'fieldsname': 'value of fieldnamd'}]

            2 - get_fields -> It return a list of field name
                Ex. ['NAME1', "KUNNIR"]

"""


class ProcessQuery(object):
    """ Class to process query sap. """

    def __init__(self, data_sap, fieldsname=None):
        self._data_sap = data_sap
        self._fieldsname = fieldsname
        self._fields = None
        self.data = self.process_data()

        def process_data(self):
            result = list()
            for row in self._data_sap:
                list_value_sap = list()
                for x in row.get('WA').split('|'):
                    list_value_sap.append(x.strip())
                result.append(dict(zip(self.get_fields(), list_value_sap)))
            return result

        def get_fields(self):
            if self._fieldsname and not self._fields:
                self._fields = [items.values()[0]
                                for items in self._fieldsname]
                return self._fields
            return
