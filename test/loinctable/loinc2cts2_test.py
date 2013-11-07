# -*- coding: utf-8 -*-
# Copyright (c) 2013, Mayo Clinic
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#     Redistributions of source code must retain the above copyright notice, this
#     list of conditions and the following disclaimer.
#
#     Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#     Neither the name of the <ORGANIZATION> nor the names of its contributors
#     may be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
import unittest
import csv

from loinctable.conversion import converter


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
            entity.append(converter.row2entity(row, "244"))

        reader.read(test_row_callback)

        return entity[0]

    def test_convert_entity_has_designation(self):
        entity = self._do_test_convert_entity().get_entity()

        self.assertEquals("R' wave amplitude.lead II", entity.classDescription.designation[0].value_.content()[0])
        self.assertEquals("PREFERRED", entity.classDescription.designation[0].designationRole)

    def test_convert_entity_has_name_namespace(self):
        entity = self._do_test_convert_entity().get_entity()

        self.assertEquals("10014-9", entity.classDescription.entityID.name)
        self.assertEquals("loincid", entity.classDescription.entityID.namespace)

    def test_convert_entity_has_type(self):
        entity = self._do_test_convert_entity().get_entity()

        type = entity.classDescription.entityType[0]
        self.assertEquals("owl", type.namespace)
        self.assertEquals("http://www.w3.org/2002/07/owl#Class", type.uri)
        self.assertEquals("Class", type.name)

    def test_convert_entity_has_alt_description_1(self):
        entity = self._do_test_convert_entity().get_entity()

        designation = entity.classDescription.designation[1]
        self.assertEquals("R' wave Amp L-II", designation.value_.content()[0])
        self.assertEquals("ALTERNATIVE", designation.designationRole)

    def test_convert_entity_has_alt_description_2(self):
        entity = self._do_test_convert_entity().get_entity()

        designation = entity.classDescription.designation[2]
        self.assertEquals("R' wave amplitude in lead II", designation.value_.content()[0])
        self.assertEquals("ALTERNATIVE", designation.designationRole)


    def test_convert_entity_entry_state(self):
        entity = self._do_test_convert_entity().get_entity()

        status = entity.classDescription.entryState
        self.assertEquals("ACTIVE", status)

    def test_convert_entity_properties(self):
        entity = self._do_test_convert_entity().get_entity()

        self.assertTrue(len(entity.classDescription.property_) > 0)