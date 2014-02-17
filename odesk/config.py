# Python bindings to oDesk API
# python-odesk version 0.5
# (C) 2010-2014 oDesk
"""Here we watch the ``PYTHON_ODESK_BASE_URL``
variable and if it is defined, use it as ``BASE_URL``.

"""

import os

BASE_URL = os.environ.get('PYTHON_ODESK_BASE_URL',
                          'https://www.odesk.com')
