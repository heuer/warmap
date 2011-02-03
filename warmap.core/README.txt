=============================================================
Warmap - A War Log (Afghanistan/Iraq) to Topic Maps converter
=============================================================


Warmap - The core package
-------------------------
The core package provides utilities which can be used to extract information
from reports::

    >>> from warmap.core import get_afghanistan_reports
    >>> 
    >>> for report in get_afghanistan_reports('./afg.csv')):
    >>>     print report.title
    >>>

The core package has no Topic Maps related code and can be used independently 
of the other packages.

