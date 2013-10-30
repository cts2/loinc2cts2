import unittest
from conversion import converter
import csv


class TestLoincReader:
    def __init__(self, csv_path):
        self.data = []
        self.csv_path = csv_path

    def read(self, row_callback):
        with open(self.csv_path, 'rb') as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter=',')
            row_callback(csvreader.next())


class EntityTest(unittest.TestCase):

    def _do_test_convert_entity(self):
        reader = TestLoincReader("data/loinc.csv")

        entity = []
        def test_row_callback(row):
            entity.append(converter.row2entity(row, lambda(x) : x, "LNC", "LNC-244", {}))

        reader.read(test_row_callback)

        return entity[0]

    def test_convert_entity_has_description(self):
        entity = self._do_test_convert_entity().as_dict()

        self.assertEquals("R' wave amplitude.lead II", entity['entityDescription']['namedEntity']['designation'][0]['value'])
        self.assertEquals("PREFERRED", entity['entityDescription']['namedEntity']['designation'][0]['designationRole'])

    def test_convert_entity_has_name_namespace(self):
        entity = self._do_test_convert_entity().as_dict()

        self.assertEquals("10014-9", entity['entityDescription']['namedEntity']['entityID']['name'])
        self.assertEquals("LNC", entity['entityDescription']['namedEntity']['entityID']['namespace'])

    def test_convert_entity_has_type(self):
        entity = self._do_test_convert_entity().as_dict()

        type = entity['entityDescription']['namedEntity']['entityType'][0]
        self.assertEquals("skos", type['namespace'])
        self.assertEquals("http://www.w3.org/2004/02/skos/core#", type['uri'])
        self.assertEquals("Concept", type['name'])

    def test_convert_entity_has_alt_description_1(self):
        entity = self._do_test_convert_entity().as_dict()

        designation = entity['entityDescription']['namedEntity']['designation'][1]
        self.assertEquals("R' wave Amp L-II", designation['value'])
        self.assertEquals("ALTERNATIVE", designation['designationRole'])

    def test_convert_entity_has_alt_description_2(self):
        entity = self._do_test_convert_entity().as_dict()

        designation = entity['entityDescription']['namedEntity']['designation'][2]
        self.assertEquals("R' wave amplitude in lead II", designation['value'])
        self.assertEquals("ALTERNATIVE", designation['designationRole'])


    def test_convert_entity_entry_state(self):
        entity = self._do_test_convert_entity().as_dict()

        status = entity['entityDescription']['namedEntity']['entryState']
        self.assertEquals("ACTIVE", status)