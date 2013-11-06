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
import sys

from utils.prettyxml import prettyxml
from ChangeSet import ChangeSetWrapper
from MAEntityDescription import MAEntityDescription
from MAAssociation import MAAssociation

class MALoincRow(object):
    def __init__(self, line):
        self.path, self.seq, self.parent, self.code, self.text = line.strip().split(',',4)


class MultiAxialLoinc(object):
    def __init__(self, filename):
        self.entries = {row.code:row for row in map(MALoincRow, open(filename))}

    def __iter__(self):
        return self.entries.itervalues()

    def parentOf(self, e):
        return self.entries.get(e.parent)



def main(args):
    if len(args) in (4,5) and args[1] in ('-e', '-a'):
        content = MultiAxialLoinc(args[2])
        if args[1] == '-e':
            rval = ChangeSetWrapper(map(lambda e: MAEntityDescription(e, args[3]), filter(lambda e:e.code.startswith('LP'), content)))
        else:
            rval = ChangeSetWrapper(map(lambda e: MAAssociation(e,args[3], content.parentOf(e)), filter(lambda e:e.parent, content)))
        if len(args) < 5 or args[4] != '-p':
            print rval.toxml()
        else:
            print prettyxml(rval)
    else:
        print "Usage: python MultiAxialLoinc.py (-e|-a) <Multi axial csv file> <LOINC version number>"


if __name__ == '__main__':
    main(sys.argv)
