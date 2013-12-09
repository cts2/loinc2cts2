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
import sys, os, argparse, codecs

_curdir = os.path.join(os.getcwd(), os.path.dirname(__file__))
sys.path.append(os.path.join(_curdir, '..'))

from multiaxialhierarchy.MAEntityDescription import MAEntityDescription
from multiaxialhierarchy.MAAssociation import MAAssociation
from multiaxialhierarchy.Skipper import skip

# This can be found in pyxb-CTS2
from utils.prettyxml import prettyxml
from common.ChangeSet import ChangeSetWrapper


class MALoincRow(object):
    def __init__(self, line):
        self.path, self.seq, self.parent, self.code, self.text = line.strip().split(',',4)


class MultiAxialLoinc(object):
    def __init__(self, filename):
        self.entries = {row.code:row for row in map(MALoincRow, skip(1,codecs.open(filename,'r',encoding="latin-1")))}

    def __iter__(self):
        return self.entries.itervalues()

    def parentOf(self, e):
        return self.entries.get(e.parent)


def main(args):
    parser = argparse.ArgumentParser(description="Generate CTS2 from LOINC MultiAxial Hierarchy")
    parser.add_argument('-e', '--entitydescriptions', action='store_true', help="Generate an EntityDescription update")
    parser.add_argument('-a', '--associations', action='store_true', help="Generate an Associations update")
    parser.add_argument('-p', '--prettyprint', action='store_true', help="Pretty print the result (takes time and memory)")
    parser.add_argument("csvfile", help="Name of CSV file to parse")
    parser.add_argument("loincver", help="LOINC Version number")
    opts = parser.parse_args(args)
    content = MultiAxialLoinc(opts.csvfile)
    eds = map(lambda e: MAEntityDescription(e, opts.loincver),
                                filter(lambda e:e.code.startswith('LP'),
                                MultiAxialLoinc(opts.csvfile))) if opts.entitydescriptions else []
    asss = map(lambda e: MAAssociation(e,opts.loincver,
                                content.parentOf(e)),
                                filter(lambda e:e.parent, MultiAxialLoinc(opts.csvfile))) if opts.associations else []

    rval = ChangeSetWrapper(eds + asss)
    print(prettyxml(rval) if opts.prettyprint else rval.toxml())

if __name__ == '__main__':
    main(sys.argv[1:])
