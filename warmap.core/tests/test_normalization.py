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
Tests against value normalization.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from warmap.core import models as m

_TEST_STRING_DATA = (
    ('HE&apos;&apos;S', "HE'S"),
    ('&amp;quot;BEARING POINT&amp;quot;', '"BEARING POINT"'),
    ('&quot;BEARING POINT&quot;', '"BEARING POINT"'),
    ('LETTER&amp;amp;apos;&amp;amp;apos;S', "LETTER'S"),
    ('', None),
    ('<null value>', None),
)

_TEST_INT_DATA = (
    ('0', 0),
    ('1', 1),
    ('', None),
)

def test_string_normalization():
    def check(content, expected):
        eq_(expected, m._none_or_string(content))
    for content, expected in _TEST_STRING_DATA:
        yield check, content, expected

def test_int_normalization():
    def check(content, expected):
        eq_(expected, m._none_or_int(content))
    for content, expected in _TEST_INT_DATA:
        yield check, content, expected


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
