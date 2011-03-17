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
Canocalization of report content.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
import re

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

def normalize_type(val):
    """\
    Returns a normalized value of the provided type.
    """
    return unicode(_TYPES.get(val.lower(), val))

def normalize_category(val):
    """\
    Returns a normalized value of the provided category.
    """
    return unicode(_CATEGORIES.get(val.lower(), val))

def normalize_classification(val):
    """\
    Returns a normalized value of the provided classification.
    """
    val = none_or_string(val)
    if val:
        val = val.upper()
    return val


_MULTIPLE_WS_PATTERN = re.compile(r' [ ]+')

def none_or_string(val):
    """\
    If the value is an emtpy string or is ``<null value>``, ``None``
    is returned. Otherwise the Unicode value.
    """
    def fix_val(val):
        # Found in the Afghanistan Diary
        return val.replace('&amp;apos;', u"'") \
                    .replace('&amp;amp;apos;', u"'") \
                    .replace('&amp;quot;', u'"') \
                    .replace('&quot;', u'"') \
                    .replace('&amp;amp;', u'&') \
                    .replace('&apos;', u"'") \
                    .replace("''", u"'")
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
    val = none_or_string(val)
    if val:
        return fn(val)
    return val

def none_or_float(val):
    """\
    Returns either ``None`` or the float value of ``val``.
    """
    return _none_or(val, float)

def none_or_int(val):
    """\
    Returns either ``None`` or the int value of ``val``.
    """
    return _none_or(val, int)

