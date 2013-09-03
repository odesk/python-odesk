"""
Python bindings to odesk API
python-odesk version 0.5
(C) 2010-2013 oDesk
"""


class Namespace(object):
    """
    A special 'proxy' class to keep API methods organized
    """

    base_url = 'https://www.odesk.com/api/'
    api_url = None
    version = 1

    def __init__(self, client):
        self.client = client

    def full_url(self, url):
        """
        Gets relative URL of API method and returns a full URL
        """
        return "{0}{1}v{2}/{3}".format(self.base_url,
                                       self.api_url, self.version, url)

    #Proxied client's methods
    def get(self, url, data=None):
        return self.client.get(self.full_url(url), data)

    def post(self, url, data=None):
        return self.client.post(self.full_url(url), data)

    def put(self, url, data=None):
        return self.client.put(self.full_url(url), data)

    def delete(self, url, data=None):
        return self.client.delete(self.full_url(url), data)


class GdsNamespace(Namespace):
    """Gds only allows GET requests."""
    base_url = 'https://www.odesk.com/gds/'

    def post(self, url, data=None):
        return None

    def put(self, url, data=None):
        return None

    def delete(self, url, data=None):
        return None
