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
from schema import core_api

loincroot = "http://id.loinc.org/"
loincns = 'loincid'
loincid = 'id/'
lpns = 'loinclp'
lpid = 'lpid/'

def uriFor(code):
    return loincroot + (lpid if code.startswith('LP') else loincid) + code

def nsFor(code):
    return lpns if code.startswith('LP') else loincns

def mahcsv(version):
    rval = core_api.CodeSystemVersionReference()
    rval.version = core_api.NameAndMeaningReference('LOINC_MAH_%s' % version)
    rval.version.uri= "http://umls.nlm.nih.gov/VSAB/LNCMAH%s" % version
    rval.codeSystem = core_api.CodeSystemReference('LOINC_MAH')
    rval.codeSystem.uri= "http://umls.nlm.nih.gov/VSAB/LNCMAH"
    return rval

def loinccsv(version):
    rval = core_api.CodeSystemVersionReference()
    rval.version = core_api.NameAndMeaningReference('LOINC_%s' % version)
    rval.version.uri= "http://umls.nlm.nih.gov/VSAB/LNC%s" % version
    rval.codeSystem = core_api.CodeSystemReference('LOINC')
    rval.codeSystem.uri= "http://umls.nlm.nih.gov/SAB/LNC"
    return rval