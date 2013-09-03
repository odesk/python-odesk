"""
Python bindings to odesk API
python-odesk version 0.5
(C) 2010-2013 oDesk
"""

import logging
import urllib2


class BaseException(Exception):
    def __init__(self, *args, **kwargs):
        self.odesk_debug(*args, **kwargs)

    def odesk_debug(self, *args, **kwargs):
        logger = logging.getLogger('python-odesk')
        logger.debug('{0}: {1}'.format(
            self.__class__.__name__,
            ', '.join(map(unicode, args))))


class BaseHttpException(urllib2.HTTPError, BaseException):

    def __init__(self, *args, **kwargs):
        self.odesk_debug(*args, **kwargs)
        super(BaseHttpException, self).__init__(*args, **kwargs)


class HTTP400BadRequestError(BaseHttpException):
    pass


class HTTP401UnauthorizedError(BaseHttpException):
    pass


class HTTP403ForbiddenError(BaseHttpException):
    pass


class HTTP404NotFoundError(BaseHttpException):
    pass


class InvalidConfiguredException(BaseException):
    pass


class APINotImplementedException(BaseException):
    pass


class AuthenticationError(BaseException):
    pass


class NotAuthenticatedError(BaseException):
    pass
