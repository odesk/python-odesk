"""
Python bindings to odesk API
python-odesk version 0.5
(C) 2010-2013 oDesk
"""
VERSION = (0, 5, 0, 'beta', 1)


def get_version():
    version = '{0}.{1}'.format(VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '{0}.{1}'.format(version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = '{0} pre-alpha'.format(version)
    else:
        if VERSION[3] != 'final':
            version = "{0} {1}".format(version, VERSION[3])
            if VERSION[4] != 0:
                version = '{0} {1}'.format(version, VERSION[4])
    return version


import os
import json
import logging
import urllib3


from odesk.oauth import OAuth
from odesk.http import raise_http_error


__all__ = ["get_version", "Client"]


logger = logging.getLogger('python-odesk')

if getattr(os.environ, "PYTHON_ODESK_DEBUG", False):
    if getattr(os.environ, "PYTHON_ODESK_DEBUG_FILE", False):
        fh = logging.FileHandler(filename=os.environ["PYTHON_ODESK_DEBUG_FILE"]
            )
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
    else:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        logger.addHandler(ch)
else:
    ch = logging.StreamHandler()
    ch.setLevel(logging.CRITICAL)
    logger.addHandler(ch)


class Client(object):
    """
    Main API client with oAuth v1 authorization.

    """

    def __init__(self, public_key, secret_key,
                 oauth_access_token=None, oauth_access_token_secret=None,
                 format_='json', finreport=True, hr=True, mc=True,
                 provider=True, task=True, team=True,
                 timereport=True, url=True, job=True):

        self.public_key = public_key
        self.secret_key = secret_key
        self.format_ = format_
        self.http = urllib3.PoolManager()

        self.oauth_access_token = oauth_access_token
        self.oauth_access_token_secret = oauth_access_token_secret

        #Namespaces
        self.auth = OAuth(self)

        if finreport:
            from odesk.routers.finreport import Finreports
            self.finreport = Finreports(self)

        if hr:
            from odesk.routers.hr import HR_V1, HR
            self.hr_v1 = HR_V1(self)
            self.hr = HR(self)

        if mc:
            from odesk.routers.mc import MC
            self.mc = MC(self)

        if provider:
            from odesk.routers.provider import Provider
            self.provider = Provider(self)

        if task:
            from odesk.routers.task import Task
            self.task = Task(self)

        if team:
            from odesk.routers.team import Team
            self.team = Team(self)

        if timereport:
            from odesk.routers.timereport import TimeReport
            self.timereport = TimeReport(self)

        if url:
            from odesk.routers.url import Url
            self.url = Url(self)

        if job:
            from odesk.routers.job import Job
            self.job = Job(self)

    #Shortcuts for HTTP methods
    def get(self, url, data=None):
        return self.read(url, data, method='GET', format_=self.format_)

    def post(self, url, data=None):
        return self.read(url, data, method='POST', format_=self.format_)

    def put(self, url, data=None):
        return self.read(url, data, method='PUT', format_=self.format_)

    def delete(self, url, data=None):
        return self.read(url, data, method='DELETE', format_=self.format_)

    # The method that actually makes HTTP requests
    def urlopen(self, url, data=None, method='GET', headers=None):

        if data is None:
            data = {}

        if headers is None:
            headers = {}

        self.last_method = method
        self.last_url = url
        self.last_data = data

        # TODO: Headers are not supported fully yet
        # instead we pass oauth parameters in querystring
        post_data = self.auth.get_oauth_params(
            url, self.oauth_access_token,
            self.oauth_access_token_secret,
            data, method)

        if method == 'GET':
            url = '{0}?{1}'.format(url, post_data)
            return self.http.urlopen(method, url)
        elif method == 'POST':
            return self.http.urlopen(
                method, url, body=post_data,
                headers={'Content-Type':
                         'application/x-www-form-urlencoded;charset=UTF-8'})
        elif method in ('PUT', 'DELETE'):
            url = '{0}?{1}'.format(url, post_data)
            headers['Content-Type'] = 'application/json'
            data_json = json.dumps(data)
            return self.http.urlopen(
                method, url, body=data_json, headers=headers)

        else:
            raise Exception('Wrong http method: {0}. Supported'
                            'methods are: '
                            'GET, POST, PUT, DELETE'.format(method))

    def read(self, url, data=None, method='GET', format_='json'):
        """
        Returns parsed Python object or raises an error
        """
        assert format_ == 'json', "Only JSON format is supported at the moment"

        if '/gds/' not in url:
            url = '{0}.{1}'.format(url, format_)

        logger = logging.getLogger('python-odesk')

        logger.debug('Prepairing to make oDesk call')
        logger.debug('URL: {0}'.format(url))
        logger.debug('Data: {0}'.format(json.dumps(data)))
        logger.debug('Method: {0}'.format(method))
        response = self.urlopen(url, data, method)

        if response.status != 200:
            logger.debug('Error: {0}'.format(response))
            raise_http_error(url, response)

        result = response.data
        logger.debug('Response: {0}'.format(result))

        if format_ == 'json':
            try:
                result = json.loads(result)
            except ValueError:
                # Not a valid json string
                logger.debug('Response is not a valid json string')
                pass
        return result


if __name__ == "__main__":
    import doctest
    doctest.testmod()
