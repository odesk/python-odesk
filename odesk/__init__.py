# Python bindings to oDesk API
# python-odesk version 0.5
# (C) 2010-2015 oDesk

# Updated by the script
"""Main package of the python bindings for oDesk API.

For convenience some most commonly used functionalities are imported here,
so you can use::

    from odesk import Client
    from odesk import raise_http_error

"""

VERSION = '0.5.6'


def get_version():
    return VERSION


from odesk.client import Client
from odesk.http import raise_http_error

__all__ = ["get_version", "Client", "raise_http_error"]
