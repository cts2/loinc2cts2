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
import uuid
import datetime

from schema.updates_api import ChangeSet, ChangeableResource
from schema.association_api import Association_
from schema.entity_api import EntityDescription_


class ChangeSetWrapper(object):

    def __init__(self, contents=None):
        self.cs = ChangeSet()
        self.cs.changeSetURI = 'urn:uuid:%s' % uuid.uuid1()
        self.cs.creationDate = datetime.datetime.now().isoformat()

        if contents:
            for e in contents:
                self.add_member(e)

    def add_member(self, e):
        cr = ChangeableResource()
        if isinstance(e, EntityDescription_):
            cr.entityDescription = e
        elif isinstance(e, Association_):
            cr.association = e
        else:
            assert False, "Unknown object type"
        cr.entryOrder = len(self.cs.member) + 1
        self.cs.append(cr)

    def get_changeset(self):
        return self.cs

    def toxml(self):
        return self.cs.toxml()


