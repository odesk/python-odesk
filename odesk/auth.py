"""
Python bindings to odesk API
python-odesk version 0.5
(C) 2010-2013 oDesk
"""


from odesk.namespaces import Namespace


class Auth(Namespace):

    api_url = 'auth/'
    version = 1

    def auth_url(self, frob=None):
        """
        Returns authentication URL to be used in a browser
        In case of desktop (non-web) application a frob is required
        """
        data = {}
        if frob:
            data['frob'] = frob
        url = 'https://www.odesk.com/services/api/auth/?' + \
            self.client.urlencode(data)
        return url

    def get_frob(self):
        """
        Gets the frob for authentication
        """
        url = 'keys/frobs'
        result = self.post(url)
        return result['frob']

    def get_token(self, frob):
        """
        Gets authentication token
        """
        url = 'keys/tokens'
        result = self.post(url, {'frob': frob})
        #TODO: Maybe there's a better way to get user's info?
        return result['token'], result['auth_user']

    def check_token(self):
        """
        Check validity of authentication token
        """
        url = 'keys/token'
        result = self.get(url)
        return result['token'], result['auth_user']

    def revoke_token(self):
        """
        Revoke authentication token
        """
        url = 'keys/token'
        data = {'api_token': self.client.api_token,
                'api_key': self.client.public_key}
        return self.delete(url, data)

    def get_info(self):
        """
        Get a detailed info about current authnticated user
        and some data from his profile.

        """
        url = 'info'
        result = self.get(url)
        return self.get('info', result)
