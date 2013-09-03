"""
Python bindings to odesk API
python-odesk version 0.5
(C) 2010-2013 oDesk
"""
from odesk.namespaces import Namespace


class Ticket(Namespace):
    api_url = 'tickets/'
    version = 1

    def get_topics(self):
        """
        Retrieve ticket topics
        """
        url = 'topics'
        result = self.get(url)
        return result.get('topics', result)

    def get_ticket(self, ticket_key):
        """
        Retrieve details of a specific ticket

        Parameters
          ticket_key    Ticket key
        """
        url = 'tickets/{0}'.format(ticket_key)
        result = self.get(url)
        return result.get('ticket', result)

    def post_new_ticket(self, message, topic_id='', topic_api_ref='',
                        email='', name=''):
        """
        Post a new ticket

        Parameters
          message
          topic_id
          topic_api_ref
          email
          name
        """
        url = 'tickets'
        data = {'message': message,
                'topic_id': topic_id,
                'topic_api_ref': topic_api_ref,
                'email': email,
                }
        result = self.post(url, data)
        return result  # TBD

    def post_reply_ticket(self, ticket_key, message):
        """
        Post reply to a specific ticket

        Parameters
          ticket_key    Ticket key
          message
        """
        url = 'tickets/{0}'.format(ticket_key)
        data = {'message': message}
        result = self.post(url, data)
        return result  # TBD
