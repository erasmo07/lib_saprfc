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


class ProcessGeneric(object):
    """ Class to process generic values of SAP. """

    def __init__(self, value_to_process):
        self._value_to_process = value_to_process

    def process_dictionary(self, dictionary):
        """ Method to process values. """
        result = dict()
        for key, value in dictionary.items():
            if isinstance(value, int):
                result.update({key: value})
            else:
                result.update({key: value.strip()})
        return result

    def list_dictionary(self):
        return [self.process_dictionary(dictionary)
                for dictionary in self._value_to_process]

    def dictionary(self):
        return self.process_dictionary(self._value_to_process)


class ProcessStructure(object):

    def __init__(self, structure):
        self._structure = structure
        self.data = self.process_values()

    def process_values(self):
        result = dict()
        for key, _object in self._structure.items():
            if isinstance(_object.value, list):
                result.update(
                    {key: ProcessGeneric(_object.value).list_dictionary()})
            elif isinstance(_object.value, dict):
                result.update({key: ProcessGeneric(_object.value).dictionary()})
            else:
                result.update({key: _object.value})
        return result


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


class ProcessError(object):

    def __init__(self, errors):
        self._errors = errors
        self._key = "ERROR"
        self.errors = self.process_data()

    def process_data(self):
        result = list()
        for dictionary in self._errors:
            result.append(dictionary.get(self._key).strip())
        return result
