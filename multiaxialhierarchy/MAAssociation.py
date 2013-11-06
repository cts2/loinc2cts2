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

from schema.association_api import Association, Association_
from schema.core_api import URIAndEntityName, PredicateReference, StatementTarget
from Constants import uriFor, nsFor, mahcsv

class MAAssociation(object):

    def __init__(self, row, version, parent=None):
        a = Association()
        a.subject = URIAndEntityName()
        a.subject.uri = uriFor(row.code)
        a.subject.namespace = nsFor(row.code)
        a.subject.name = str(row.code)
        a.subject.designation = row.text

        a.predicate = PredicateReference()
        a.predicate.uri = "http://www.w3.org/2004/02/skos/core#broaderTransitive"
        a.predicate.namespace = "skos"
        a.predicate.name = "broaderTransitive"

        t = URIAndEntityName()
        t.uri = uriFor(row.parent)
        t.namespace = nsFor(row.parent)
        t.name = str(row.parent)
        if parent:
            t.designation = parent.text
        a.target.append(StatementTarget(t))


        a.assertedBy = mahcsv(version)
        self.val = a


    def toxml(self):
        return self.val.toxml()