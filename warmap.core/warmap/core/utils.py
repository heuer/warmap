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
Utility functions for the war logs

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from __future__ import with_statement
import csv
import itertools
from warmap.core.models import Report

def get_afghanistan_reports(filename):
    """\
    Returns a generator which returns ``models.Report`` instances.

    `filename`
        The filename to read the dataset from.
    """
    return (Report(row) for row in get_afghanistan_rows(filename))

def get_afghanistan_rows(filename):
    """\
    Returns a generator over the rows of the Afghanistan log datatset.

    `filename`
        The filename to read the dataset from.
    """
    with open(filename, 'rb') as f:
        for row in csv.reader(f, delimiter=',', quotechar='"'):
            if row:
                yield row

def get_iraq_reports(filename, omitheader=True):
    """\
    Returns a generator which returns ``models.Report`` instances.

    `filename`
        The filename to read the dataset from.

    `omitheader`
        Indicates if the first row of the dataset should be omitted
        (``True`` by default)
    """
    return (Report(row) for row in get_iraq_rows(filename, omitheader))

def get_iraq_rows(filename, omitheader=True):
    """\
    Returns a generator over the rows of the Iraq log datatset.

    `filename`
        The filename to read the dataset from.

    `omitheader`
        Indicates if the first row of the dataset should be omitted
        (``True`` by default)
    """
    with open(filename, 'rb') as f:
        reader = csv.reader(f, quotechar='"', escapechar='\\')
        iterator = itertools.islice(reader, 1, None) if omitheader else reader
        for row in iterator:
            if row:
                yield row
