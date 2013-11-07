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

not_properties = {'LOINC_NUM', 'COMPONENT', 'SHORTNAME',
                  'LONG_COMMON_NAME', 'STATUS', 'COMMENTS',
                  'EXMPL_ANSWERS', 'EXAMPLE_UNITS',
                  'EXAMPLE_UCUM_UNITS', 'EXAMPLE_SI_UCUM_UNITS'}


def row2entity(row, code_system_version):
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

    return entity
