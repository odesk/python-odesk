"""
Python bindings to odesk API
python-odesk version 0.5
(C) 2010-2013 oDesk
"""
from odesk.namespaces import Namespace


class Team(Namespace):

    api_url = 'team/'
    version = 1

    def get_snapshot(self, company_id, user_id, datetime=None):
        """
        Retrieve a company's user snapshots during given time or 'now'

        Parameters:
          company_id    The Company ID
          user_id       The User ID
          datetime      (default 'now') Timestamp either a datetime
                        object
                        or a string in ISO 8601 format (in UTC)
                        yyyymmddTHHMMSSZ
                        or a string with UNIX timestamp (number of
                        seconds after epoch)
        """
        url = 'snapshots/{0}/{1}'.format(company_id, user_id)
        if datetime:   # date could be a list or a range also
            url = '{0}/{1}'.format(url, datetime.isoformat())
        result = self.get(url)
        if 'snapshot' in result:
            snapshot = result['snapshot']
        else:
            snapshot = []
        if 'error' in result:
            return result
        return snapshot

    def update_snapshot(self, company_id, user_id, datetime=None,
                        memo=''):
        """
        Update a company's user snapshot memo at given time or 'now'

        Parameters:
          company_id    The Company ID
          user_id       The User ID
          datetime      (default 'now') Timestamp either a datetime
                        object
                        or a string in ISO 8601 format (in UTC)
                        yyyymmddTHHMMSSZ
                        or a string with UNIX timestamp (number of
                        seconds after epoch)
          memo          The Memo text
        """
        url = 'snapshots/{0}/{1}'.format(company_id, user_id)
        if datetime:
            url = '{0}/{1}'.format(url, datetime.isoformat())
        return self.post(url, {'memo': memo})

    def delete_snapshot(self, company_id, user_id, datetime=None):
        """
        Delete a company's user snapshot memo at given time or 'now'

        Parameters:
          company_id    The Company ID
          user_id       The User ID
          datetime      (default 'now') Timestamp either a datetime
                        object
                        or a string in ISO 8601 format (in UTC)
                        yyyymmddTHHMMSSZ
                        or a string with UNIX timestamp (number of
                        seconds after epoch)
        """
        url = 'snapshots/{0}/{1}'.format(company_id, user_id)
        if datetime:
            url = '{0}/{1}'.format(url, datetime.isoformat())
        return self.delete(url)

    def get_workdiaries(self, team_id, username, date=None):
        """
        Retrieve a team member's workdiaries for given date or today

        Parameters:
          team_id       The Team ID
          username      The Team Member's username
          date          A datetime object or a string in yyyymmdd
                        format (optional)
        """
        url = 'workdiaries/{0}/{1}'.format(team_id, username)
        if date:
            url = '{0}/{1}'.format(url, date)
        result = self.get(url)
        if 'error' in result:
            return result

        snapshots = result.get('snapshots', {}).get('snapshot', [])
        if not isinstance(snapshots, list):
            snapshots = [snapshots]
        #not sure we need to return user
        return result['snapshots']['user'], snapshots

    def get_teamrooms(self, target_version=1):
        """
        Retrieve all teamrooms accessible to the authenticated user

        Parameters:
            target_version      Version of future requested API
        """
        url = 'teamrooms'

        current_version = self.version
        if target_version != current_version:
            self.version = target_version
        result = self.get(url)
        if 'error' in result:
            return result

        if 'teamrooms' in result and 'teamroom' in result['teamrooms']:
            teamrooms = result['teamrooms']['teamroom']
        else:
            teamrooms = []
        if not isinstance(teamrooms, list):
            teamrooms = [teamrooms]
        if target_version != current_version:
            self.version = current_version
        return teamrooms

    def get_snapshots(self, team_id, online='now', target_version=1):
        """
        Retrieve team member snapshots

        Parameters:
          team_id           The Team ID
          online            'now' / 'last_24h' / 'all' (default 'now')
                            Filter for logged in users / users active in
                            last 24 hours / all users
          target_version    Version of future requested API
        """
        url = 'teamrooms/{0}'.format(team_id)
        current_version = self.version
        if target_version != current_version:
            self.version = target_version

        result = self.get(url, {'online': online})
        if 'error' in result:
            return result

        if 'teamroom' in result and 'snapshot' in result['teamroom']:
            snapshots = result['teamroom']['snapshot']
        else:
            snapshots = []
        if not isinstance(snapshots, list):
            snapshots = [snapshots]
        if target_version != current_version:
            self.version = current_version
        return snapshots
