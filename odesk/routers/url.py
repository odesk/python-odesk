"""
Python bindings to odesk API
python-odesk version 0.5
(C) 2010-2013 oDesk
"""

from odesk.namespaces import Namespace


class Url(Namespace):
    api_url = 'shorturl/'
    version = 1

    def get_shorten(self, long_url):
        url = 'shorten'
        data = {'url': long_url}
        result = self.get(url, data=data)
        return result.get('short_url', result)

    def get_expand(self, short_url):
        url = 'expand'
        data = {'url': short_url}
        result = self.get(url, data=data)
        return result.get('long_url', result)
