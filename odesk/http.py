# Python bindings to oDesk API
# python-odesk version 0.5
# (C) 2010-2014 oDesk

import logging
import urllib2
import httplib

from odesk.exceptions import HTTP400BadRequestError, HTTP401UnauthorizedError,\
    HTTP403ForbiddenError, HTTP404NotFoundError

ODESK_ERROR_CODE = 'x-odesk-error-code'
ODESK_ERROR_MESSAGE = 'x-odesk-error-message'


__all__ = ['raise_http_error']


def raise_http_error(url, response):
    """Raise custom ``urllib2.HTTPError`` exception.

    *Parameters:*
      :url:         Url that caused an error

      :response:    ``urllib3`` response object

    """
    status_code = response.status

    headers = response.getheaders()
    odesk_error_code = headers.get(ODESK_ERROR_CODE, 'N/A')
    odesk_error_message = headers.get(ODESK_ERROR_MESSAGE, 'N/A')

    formatted_msg = 'Code {0}: {1}'.format(odesk_error_code,
                                           odesk_error_message)

    if status_code == httplib.BAD_REQUEST:
        raise HTTP400BadRequestError(url, status_code, formatted_msg,
                                     headers, None)
    elif status_code == httplib.UNAUTHORIZED:
        raise HTTP401UnauthorizedError(url, status_code, formatted_msg,
                                       headers, None)
    elif status_code == httplib.FORBIDDEN:
        raise HTTP403ForbiddenError(url, status_code, formatted_msg,
                                    headers, None)
    elif status_code == httplib.NOT_FOUND:
        raise HTTP404NotFoundError(url, status_code, formatted_msg,
                                   headers, None)
    else:
        error = urllib2.HTTPError(url, status_code, formatted_msg,
                                  headers, None)
        logger = logging.getLogger('python-odesk')
        logger.debug(str(error))
        raise error
