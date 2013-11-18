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
from cts2_types import *
from schema.core_api import StatementTarget, AnonymousStatement
from common.Constants import uriForProperty, uriForOwl, owlns, lprns

not_properties = {'LOINC_NUM', 'COMPONENT', 'SHORTNAME',
                  'LONG_COMMON_NAME', 'STATUS', 'COMMENTS',
                  'EXMPL_ANSWERS', 'EXAMPLE_UNITS',
                  'EXAMPLE_UCUM_UNITS', 'EXAMPLE_SI_UCUM_UNITS'}

def _create_owl_predicate(name):
    p = PredicateReference()
    p.name = name
    p.uri = uriForOwl(p.name)
    p.namespace = owlns
    return p

def _create_lnc_predicate(name):
    p = PredicateReference()
    p.name = name
    p.uri = uriForProperty(p.name)
    p.namespace = lprns
    return p

intersection_predicate = _create_owl_predicate("intersectionOf")
hascomponent_predicate = _create_owl_predicate("hasComponent")
somevaluesfrom_predicate = _create_owl_predicate("someValuesFrom")
allvaluesfrom_predicate = _create_owl_predicate("allValuesFrom")
equivalentclass_predicate = _create_owl_predicate("equivalentClass")
hasscale_prediate = _create_lnc_predicate("hasScale")
hassystem_prediate = _create_lnc_predicate("hasSystem")
hastime_prediate = _create_lnc_predicate("hasTime")
hasproperty_prediate = _create_lnc_predicate("hasProperty")
hasmethod_prediate = _create_lnc_predicate("hasMethod")

def row2entity(row, code_system_version):
    try:
        name = row['LOINC_NUM']
        description = row['COMPONENT']
        short_name = row['SHORTNAME']
        long_common_name = row['LONG_COMMON_NAME']
        status = row['STATUS']
        comments = row['COMMENTS']
        example_answers = row['EXMPL_ANSWERS']
        example_units = row['EXAMPLE_UNITS']
        example_ucum_units = row['EXAMPLE_UCUM_UNITS']
        example_si_ucum_units = row['EXAMPLE_SI_UCUM_UNITS']

        # TODO: Individual copyrights for Entities -- how to handle
        copyright = row['EXTERNAL_COPYRIGHT_NOTICE']

        entity = EntityWrapper(name=name, code_system_version=code_system_version)
        entity.add_designation(description)
        entity.add_designation(short_name, False)
        entity.add_designation(long_common_name, False)
        entity.add_note(comments)
        entity.add_example(example_answers)
        entity.add_example(example_units)
        entity.add_example(example_ucum_units)
        entity.add_example(example_si_ucum_units)
        entity.set_status(status)

        for k, v in filter(lambda (k, v): k not in not_properties and v, row.iteritems()):
            entity.add_property(k, v)

    except UnicodeDecodeError:
        print "Error Decoding Entity text."
        return None

    return entity

def row2association(row, code_system_version):
    try:
        subject = row['LOINC_NUM']
        description = row['COMPONENT']

        association = AssociationWrapper(subject, description, code_system_version)

        association.predicate = equivalentclass_predicate

        bnode = AnonymousStatement(predicate=intersection_predicate,
                                   target=[
                                       StatementTarget(_inner_bnode(hascomponent_predicate, row['COMPONENT'])),
                                       StatementTarget(_inner_bnode(hasmethod_prediate, row['METHOD_TYP'])),
                                       StatementTarget(_inner_bnode(hasproperty_prediate, row['PROPERTY'])),
                                       StatementTarget(_inner_bnode(hastime_prediate, row['TIME_ASPCT'])),
                                       StatementTarget(_inner_bnode(hassystem_prediate, row['SYSTEM'])),
                                       StatementTarget(_inner_bnode(hasscale_prediate, row['SCALE_TYP'])),
                                    ])

        association.target.append(StatementTarget(bnode))

    except UnicodeDecodeError:
        print "Error Decoding Association text."
        return None

    return association


def _inner_bnode(predicate, name):
    return AnonymousStatement(predicate=intersection_predicate, target=_somevalues_allvalues(predicate, name))


def _somevalues_allvalues(predicate, name):
    t = URIAndEntityName()
    t.uri = uriForProperty(name)
    t.namespace = lprns
    t.name = name

    return [StatementTarget(AnonymousStatement(
        predicate=predicate,
        target=[StatementTarget(
            AnonymousStatement(
                predicate=p,
                target=[StatementTarget(t)]))])) for p in [somevaluesfrom_predicate, allvaluesfrom_predicate]]
