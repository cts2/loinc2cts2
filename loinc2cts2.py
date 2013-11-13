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
import argparse
from loinctable.LoincTable import LoincTable
from multiaxialhierarchy import MultiAxialLoinc, MAAssociation, MAEntityDescription
from common.ChangeSet import ChangeSetWrapper
from rest import cts2_rest_client
import sys, os, errno, itertools


def _write_change_set(wrapper, output, url):
    uri = wrapper.get_changeset().changeSetURI

    if url is not None:
        cts2_rest_client.put_changeset(url, wrapper)

    with open(output + "/" + uri + ".xml", 'w') as the_file:
        the_file.write(wrapper.toxml())

def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def chunks(itr, chunk):
    while True:
        slice = itertools.islice(itr, chunk)
        if not slice:
            return
        yield slice

def main(args):
    parser = argparse.ArgumentParser(description='CTS2 LOINC Converter')
    parser.add_argument('-ma', help='the LOINC MultiAxial Hierarchy CSV file')
    parser.add_argument('-lt', help='the LOINC Table CSV file')
    parser.add_argument('-o',  help='the output directory for CTS2 ChangeSets')
    parser.add_argument('-url', help='the CTS2 URL to PUT the ChangeSets to')
    parser.add_argument('loinc_version', help='the LOINC Version Identifier')

    args = parser.parse_args()
    output_dir = args.o
    loinc_version = args.loinc_version
    url = args.url
    lt = args.lt
    ma = args.ma

    mkdir(output_dir)

    changeset_size = 100

    if lt:
        loinc_table = LoincTable(lt, loinc_version)

        for changeset_wrapper in loinc_table.to_cts2(changeset_size):
            _write_change_set(changeset_wrapper, output_dir, url)

    if ma:
        multi_axial = MultiAxialLoinc.MultiAxialLoinc(ma)

        content_itr = multi_axial.__iter__()

        for content in chunks(content_itr, changeset_size):
            entities = ChangeSetWrapper(map(lambda e: MAEntityDescription.MAEntityDescription(e, loinc_version), filter(lambda e:e.code.startswith('LP'), content)))
            associations = ChangeSetWrapper(map(lambda e: MAAssociation.MAAssociation(e, loinc_version, multi_axial.parentOf(e)), filter(lambda e:e.parent, content)))

            map(lambda x: _write_change_set(x, output_dir, url), [entities, associations])


if __name__ == '__main__':
    main(sys.argv)