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
import abc

from schema import entity_api, core_api
from schema.core_api import Example, Property, Comment, PredicateReference
from model.Designation import Designation
import pyxb
from common.Constants import uriFor, nsFor, loinccsv


class Cts2TypeWrapper():
    @abc.abstractmethod
    def toxml(self):
        raise NotImplementedError("Please implement the 'toxml' method on all Cts2TypeWrappers.")


class EntityWrapper(Cts2TypeWrapper):
    statuses_map = {
        "ACTIVE": "ACTIVE",
        "TRIAL": "ACTIVE",
        "DISCOURAGED": "ACTIVE",
        "DEPRECATED": "INACTIVE"
    }

    def __init__(self, name, code_system_version):
        e = entity_api.ClassDescription()
        e.about = uriFor(name)
        e.entityID = core_api.ScopedEntityName()
        e.entityID.namespace = nsFor(name)
        e.entityID.name = name
        e.describingCodeSystemVersion = loinccsv(code_system_version)

        et = core_api.URIAndEntityName()
        et.uri = 'http://www.w3.org/2002/07/owl#Class'
        et.namespace = 'owl'
        et.name = 'Class'
        e.entityType.append(et)
        self.val = entity_api.EntityDescription()
        self.val.classDescription = e

    def get_entity(self):
        return self.val

    def add_designation(self, description, is_preferred=True):
        if not description:
            return
        self.val.classDescription.designation.append(Designation(description, is_preferred))

    def add_note(self, note_value):
        if not note_value:
            return
        comment = Comment()
        comment.value_ = note_value
        self.val.classDescription.note.append(comment)

    def add_example(self, example_value):
        if not example_value:
            return
        example = Example()
        example.value_ = example_value
        self.val.classDescription.example.append(example)

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
            property.value_ = property_value
            self.val.classDescription.property_.append(property)
        except pyxb.exceptions_.MixedContentError:
            print "ERROR Loading Property: {name = '%s', value = '%s'}" % (property_name, property_value)


    def set_status(self, status="ACTIVE"):
        pass

    def toxml(self):
        return self.val.toxml()


class CodeSystemWrapper(Cts2TypeWrapper):
    def __init__(self, about, name):
        pass

    def toxml(self):
        return self.val.toxml()