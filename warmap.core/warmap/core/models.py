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
import re
from operator import itemgetter

_MULTIPLE_WS_PATTERN = re.compile(r' [ ]+')

# Constants which refer to a column in the CSV dataset
KEY = 0
CREATED = 1
TYPE = 2
CATEGORY = 3
TRACKING_NUMBER = 4
TITLE = 5
SUMMARY = 6
REGION = 7
ATTACK_ON = 8
COMPLEX_ATTACK = 9
REPORTING_UNIT = 10
UNIT_NAME = 11
TYPE_OF_UNIT = 12
FRIENDLY_WIA = 13
FRIENDLY_KIA = 14
HOST_NATION_WIA = 15
HOST_NATION_KIA = 16
CIVILIAN_WIA = 17
CIVILIAN_KIA = 18
ENEMY_WIA = 19
ENEMY_KIA = 20
ENEMY_DETAINED = 21
MGRS = 22
LATITUDE = 23
LONGITUDE = 24
ORIGINATOR_GROUP = 25
UPDATED_BY_GROUP = 26
CCIR = 27
SIGACT = 28
AFFILIATION = 29
DCOLOR = 30
CLASSIFICATION = 31

# Used to canonicalize the report type
_TYPES = {
    '': u'None Selected', #TODO: Is that okay?
    'explosive hazard': u'Explosive Hazard',
    'friendly fire': u'Friendly Fire',
    'friendly action': u'Friendly Action',
    'criminal event': u'Criminal Event',
    'other': u'Other',
    'non-combat event': u'Non-Combat Event',
    'counter insurgency': u'Counter-Insurgency',
}

# Used to canonicalize the report category
_CATEGORIES = {
    '': u'None Selected', #TODO: Is that okay?
    '<null value>': u'None Selected', #TODO: Is that okay?
    'other': 'Other',
    'blue-blue': 'Blue-Blue',
    'blue-green': 'Blue-Green',
    'green-blue': 'Green-Blue',
    'green-green': 'Green-Green',
    'blue-on-white': 'Blue-On-White', #TODO: Is this the same as Blue-White?
    'Counter Insurgency': u'Counter-Insurgency',
    'ied hoax': 'IED Hoax',
    'murder': 'Murder',
    'arrest': 'Arrest',
    'smuggling': 'Smuggling',
    'other offensive': 'Other Offensive',
    'unexploded ordnance': 'Unexploded Ordnance',
    'accident': 'Accident',
    'raid': 'Raid',
    'attack': 'Attack',
    'attack threat': 'Attack Threat',
    'green-white': 'Green-White',
    'ied suspected': 'IED Suspected',
    'kidnapping': 'Kidnapping',
    'confiscation': 'Confiscation',
    'detain': 'Detain',
    'meeting': 'Meeting',
    'explosive remnants of war (erw)/turn in': 'Explosive Remnants of War (ERW)/Turn In',
    'indirect fire threat': 'Indirect Fire Threat',
    'indirect fire': 'Indirect Fire',
    'direct fire': 'Direct Fire',
    'ied found/cleared': 'IED Found/Cleared',
    'equipment failure': 'Equipment Failure',
    'sniper ops': 'Sniper Ops',
    'other defensive': 'Other Defensive',
    'medevac': 'MEDEVAC',
    'supporting cf': 'Supporting CF',
    'escalation of force': 'Escalation of Force',
    'unknown explosion': 'Unknown Explosion',
    'cordon/search': 'Cordon/Search',
    'explosive remnants of war (erw) found/cleared': 'Explosive Remnants of War (ERW) Found/Cleared',
    'tests of security': 'Tests of Security',
    'ied explosion': 'IED Explosion',
    'cache found/cleared': 'Cache Found/Cleared',
    'lasing': 'Lasing',
    'police actions': 'Police Actions',
}

def _normalize_type(val):
    """\
    Returns a normalized value of the provided type.
    """
    return unicode(_TYPES.get(val.lower(), val))

def _normalize_category(val):
    """\
    Returns a normalized value of the provided category.
    """
    return unicode(_CATEGORIES.get(val.lower(), val))

def _normalize_classification(val):
    """\
    Returns a normalized value of the provided classification.
    """
    val = _none_or_string(val)
    if val:
        val = val.upper()
    return val

def _none_or_string(val):
    """\
    If the value is an emtpy string or is ``<null value>``, ``None``
    is returned. Otherwise the Unicode value.
    """
    def fix_val(val):
        # Found in the Afghanistan Diary
        return val.replace('&amp;apos;', u"'") \
                    .replace('&amp;amp;apos;', u"'") \
                    .replace('&amp;quot;', u'"') \
                    .replace('&amp;amp;', u'&')
    if val:
        val = _MULTIPLE_WS_PATTERN.sub(' ', val.strip())
    if val in ('', '<null value>'):
        return None
    return unicode(fix_val(val))

def _none_or(val, fn):
    """\
    If the value is an emtpy string or is ``<null value>``, ``None``
    is returned. Otherwise the function ``fn`` is applied to the
    Unicode value.
    """
    val = _none_or_string(val)
    if val:
        return fn(val)
    return val

def _none_or_float(val):
    """\
    Returns either ``None`` or the float value of ``val``.
    """
    return _none_or(val, float)

def _none_or_int(val):
    """\
    Returns either ``None`` or the int value of ``val``.
    """
    return _none_or(val, int)

_COLUMN_TO_DATATYPE = {
    KEY: unicode,
    CREATED: unicode,
    TYPE: _normalize_type,
    CATEGORY: _normalize_category,
    TRACKING_NUMBER: _none_or_string,
    TITLE: _none_or_string,
    SUMMARY: _none_or_string,
    REGION: _none_or_string,
    ATTACK_ON: _none_or_string,
    COMPLEX_ATTACK: lambda x: x.upper() == 'TRUE',
    REPORTING_UNIT: _none_or_string,
    UNIT_NAME: _none_or_string,
    TYPE_OF_UNIT: _none_or_string,
    FRIENDLY_WIA: _none_or_int, 
    FRIENDLY_KIA: _none_or_int,
    HOST_NATION_WIA: _none_or_int,
    HOST_NATION_KIA: _none_or_int,
    CIVILIAN_WIA: _none_or_int,
    CIVILIAN_KIA: _none_or_int,
    ENEMY_WIA: _none_or_int,
    ENEMY_KIA: _none_or_int,
    ENEMY_DETAINED: _none_or_int,
    MGRS: _none_or_string,
    LATITUDE: _none_or_float,
    LONGITUDE: _none_or_float,
    ORIGINATOR_GROUP: _none_or_string,
    UPDATED_BY_GROUP: _none_or_string,
    CCIR: _none_or_string,
    SIGACT: _none_or_string,
    AFFILIATION: _none_or_string,
    DCOLOR: lambda x: unicode(x.upper()),
    CLASSIFICATION: _normalize_classification,
}

def _prop(idx):
    return property(itemgetter(idx))

class Report(tuple):
    """\
    Immutable class which represents one war report.
    """
    __slots__ = ()
    
    def __new__(cls, values):
        if len(values) == 34: # Iraq report
            values = values[2:]
        if len(values) != 32:
            raise ValueError('Expected a tuple/list with a length of 32, got %s' % len(values))
        return tuple.__new__(cls, [_COLUMN_TO_DATATYPE[i](v) for i, v in enumerate(values)])

    def items(self):
        """\
        Returns a generator which provides all properties and their values.
        Example: ``('key', u'the-report-key-value')`` 
        """
        for name in (attr for attr in dir(self) if attr[:2] != '__'):
            value = getattr(self, name)
            if callable(value):
                continue
            yield name, value
 
    key = _prop(KEY)
    created = _prop(CREATED)
    type = _prop(TYPE)
    category = _prop(CATEGORY)
    tracking_number = _prop(TRACKING_NUMBER)
    title = _prop(TITLE)
    summary = _prop(SUMMARY)
    region = _prop(REGION)
    attack_on = _prop(ATTACK_ON)
    complex_attack = _prop(COMPLEX_ATTACK)
    reporting_unit = _prop(REPORTING_UNIT)
    unit_name = _prop(UNIT_NAME)
    type_of_unit = _prop(TYPE_OF_UNIT)
    friendly_wia = _prop(FRIENDLY_WIA)
    friendly_kia = _prop(FRIENDLY_KIA)
    host_nation_wia = _prop(HOST_NATION_WIA)
    host_nation_kia = _prop(HOST_NATION_KIA)
    civilian_wia = _prop(CIVILIAN_WIA)
    civilian_kia = _prop(CIVILIAN_KIA)
    enemy_wia = _prop(ENEMY_WIA)
    enemy_kia = _prop(ENEMY_KIA)
    enemy_detained = _prop(ENEMY_DETAINED)
    mgrs = _prop(MGRS)
    latitude = _prop(LATITUDE)
    longitude = _prop(LONGITUDE)
    originator_group = _prop(ORIGINATOR_GROUP)
    updated_by_group = _prop(UPDATED_BY_GROUP)
    ccir = _prop(CCIR)
    sigact = _prop(SIGACT)
    affiliation = _prop(AFFILIATION)
    dcolor = _prop(DCOLOR)
    classification = _prop(CLASSIFICATION)
