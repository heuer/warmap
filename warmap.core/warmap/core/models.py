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
This module provides classes to keep data about reports.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from operator import itemgetter
from itertools import chain
from warmap.core import constants
from warmap.core.c14n import normalize_type, normalize_category, normalize_classification, \
                             none_or_string, none_or_int, none_or_float

_NORMALIZER = (
        unicode, unicode, normalize_type, normalize_category, none_or_string,
        none_or_string, none_or_string, none_or_string, none_or_string,  lambda x: x.upper() == 'TRUE',
        none_or_string, none_or_string, none_or_string, none_or_int, none_or_int,
        none_or_int, none_or_int, none_or_int, none_or_int, none_or_int,
        none_or_int, none_or_int, none_or_string, none_or_float, none_or_float,
        none_or_string, none_or_string, none_or_string, none_or_string, none_or_string,
        lambda x: unicode(x.upper()), normalize_classification, int)

_PROPERTY_NAMES = (
        'key', 'created', 'type', 'category', 'tracking_number',
        'title', 'summary', 'region', 'attack_on', 'complex_attack',
        'reporting_unit', 'unit_name', 'type_of_unit', 'friendly_wia', 'friendly_kia',
        'host_nation_wia', 'host_nation_kia', 'civilian_wia', 'civilian_kia', 'enemy_wia',
        'enemy_kia', 'enemy_detained', 'mgrs', 'latitude', 'longitude',
        'originator_group', 'updated_by_group', 'ccir', 'sigact', 'affiliation',
        'dcolor', 'classification', 'kind')

class Report(tuple):
    """\
    Immutable class which represents one war report.
    """
    __slots__ = ()
    
    def __new__(cls, values, kind=None):
        if len(values) == 34: # Iraq report
            values = values[2:]
            if kind is None:
                kind = constants.KIND_IQ
        elif kind is None:
            kind = constants.KIND_AF
        if len(values) != 32:
            raise ValueError('Expected a tuple/list with a length of 32, got %s' % len(values))
        return tuple.__new__(cls, [_NORMALIZER[i](v) for i, v in enumerate(chain(values, (kind,)))])

    def items(self):
        """\
        Returns a generator which provides all properties and their values.
        Example: ``('key', u'the-report-key-value')`` 
        """
        for i, name in enumerate(_PROPERTY_NAMES):
            yield name, self[i]

for i, name in enumerate(_PROPERTY_NAMES):
    setattr(Report, name, property(itemgetter(i)))
