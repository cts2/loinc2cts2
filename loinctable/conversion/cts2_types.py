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


from schema.entity_api import EntityDescription_, ClassDescription
from schema.association_api import Association_
from schema.codesystem_api import CodeSystemCatalogEntry_
from schema.core_api import Example, Property, Comment, PredicateReference, ScopedEntityName, URIAndEntityName, \
    StatementTarget, Note, EntryDescription
from model.Designation import Designation, OpaqueData
import pyxb
from common.Constants import uriFor, nsFor, loinccsv, mahcsv



class EntityWrapper(EntityDescription_):
    statuses_map = {
        "ACTIVE": "ACTIVE",
        "TRIAL": "ACTIVE",
        "DISCOURAGED": "ACTIVE",
        "DEPRECATED": "INACTIVE"
    }

    def __init__(self, name, code_system_version):
        EntityDescription_.__init__(self)
        e = ClassDescription()
        e.about = uriFor(name)
        e.entityID = ScopedEntityName()
        e.entityID.namespace = nsFor(name)
        e.entityID.name = name
        e.describingCodeSystemVersion = loinccsv(code_system_version)

        et = URIAndEntityName()
        et.uri = 'http://www.w3.org/2002/07/owl#Class'
        et.namespace = 'owl'
        et.name = 'Class'
        e.entityType.append(et)
        self.classDescription = e

    def add_designation(self, description, is_preferred=True):
        if not description:
            return
        self.classDescription.designation.append(Designation(description, is_preferred))

    def add_note(self, note_value):
        if not note_value:
            return
        self.classDescription.note.value_ = OpaqueData(note_value)

    def add_example(self, example_value):
        if not example_value:
            return
        self.classDescription.example.value_ = OpaqueData(example_value)

    def add_property(self, property_name, property_value):
        if not property_value:
            return
        try:
            property = Property()
            predicate = PredicateReference()
            predicate.name = property_name
            predicate.namespace = nsFor(property_name)
            predicate.uri = uriFor(property_name)
            property.predicate = predicate
            st = StatementTarget()
            st.literal = OpaqueData(property_value)
            property.value_.append(st)
            self.classDescription.property_.append(property)
        except:
            print "ERROR Loading Property: {name = '%s', value = '%s'}" % (property_name, property_value)

    def set_status(self, status="ACTIVE"):
        if status in self.statuses_map:
            self.classDescription.entryState = self.statuses_map[status]



class CodeSystemWrapper(CodeSystemCatalogEntry_):
    def __init__(self, about, name):
        CodeSystemCatalogEntry_.__init__(self)


class AssociationWrapper(Association_):

    def __init__(self, subject_name, subject_description, code_system_version):
        Association_.__init__(self)
        self.subject = URIAndEntityName()
        self.subject.uri = uriFor(subject_name)
        self.subject.namespace = nsFor(subject_name)
        self.subject.name = subject_name
        self.subject.designation = subject_description

        self.assertedBy = loinccsv(code_system_version)

    def add_target(self, target):
        self.target.append(target)