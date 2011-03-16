# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
#     * Neither the project name nor the names of the contributors may be 
#       used to endorse or promote products derived from this software 
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
"""\
Tests against models.Report

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_, raises
from warmap.core import models

_TEST_DATA = (
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', 'FALSE', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'],
    ['garbage', 'more-garbage', '0', '1', '2', '3', '4', '5', '6', '7', '8', 'TRUE', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
)

_TEST_DATA_ILLEGAL = (
    map(str, range(0, 31)),
    map(str, range(0, 35)),
)

def test_tuple_legal():
    def check(data):
        report = models.Report(data)
        offset = 0
        if len(data) == 34:
            offset=2
        for i, name in enumerate(models._PROPERTY_NAMES):
            value = data[i+offset]
            if i in (13, 14, 15, 16, 17, 18, 19, 20, 21, 23):
                value = int(value)
            elif i == 24:
                value = float(value)
            elif i == 9:
                value = value == 'TRUE'
            eq_(value, report[i])
            eq_(value, getattr(report, name))
    for data in _TEST_DATA:
        yield check, data

def test_tuple_illegal():
    @raises(ValueError)
    def check(data):
        models.Report(data)
    for data in _TEST_DATA_ILLEGAL:
        yield check, data

if __name__ == '__main__':
    import nose
    nose.core.runmodule()
