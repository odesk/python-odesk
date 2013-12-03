# Python bindings to oDesk API
# python-odesk version 0.5
# (C) 2010-2013 oDesk

import urllib


from odesk.namespaces import Namespace


class Task(Namespace):
    api_url = 'otask/'
    version = 1

    def get_company_tasks(self, company_id):
        """
        Retrieve a list of all tasks assigned within a company.

        The user authenticated must have been granted the appropriate
        hiring manager permissions.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.
        """
        url = 'tasks/companies/{0}/tasks'.format(company_id)
        result = self.get(url)
        try:
            return result["tasks"] or []
        except KeyError:
            return result

    def get_team_tasks(self, company_id, team_id):
        """
        Retrieve a list of all tasks assigned to a team.

        The user authenticated must have been granted the appropriate
        hiring manager permissions.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :team_id:       Team ID. Use the 'id' value
                          from ``hr.get_team()`` API call.

        """
        url = 'tasks/companies/{0}/teams/{1}/tasks'.format(company_id,
                                                           team_id)
        result = self.get(url)
        try:
            return result["tasks"] or []
        except KeyError:
            return result

    def get_user_tasks(self, company_id, team_id, user_id):
        """
        Retrieve a list of all tasks assigned to a team member.

        The user authenticated must have been granted the appropriate
        hiring manager permissions.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :team_id:       Team ID. Use the 'id' value
                          from ``hr.get_team()`` API call.

          :user_id:       User ID

        """
        url = 'tasks/companies/{0}/teams/{1}/users/{2}/tasks'.format(
            company_id, team_id, user_id)
        result = self.get(url)
        try:
            return result["tasks"] or []
        except KeyError:
            return result

    def get_company_tasks_full(self, company_id):
        """
        Retrieve full list of all tasks assigned within a company \
        (with detail of level at which the task is assigned).

        The user authenticated must have been granted the appropriate
        hiring manager permissions.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

        """
        url = 'tasks/companies/{0}/tasks/full_list'.format(company_id)
        result = self.get(url)
        try:
            return result["tasks"] or []
        except KeyError:
            return result

    def get_team_tasks_full(self, company_id, team_id):
        """
        Retrieve a list of all tasks assigned to a team \
        (with detail of level at which the task is assigned).

        The user authenticated must have been granted the appropriate
        hiring manager permissions.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :team_id:       Team ID. Use the 'id' value
                          from ``hr.get_team()`` API call.

        """
        url = 'tasks/companies/{0}/teams/{1}/tasks/full_list'.format(
            company_id, team_id)
        result = self.get(url)
        try:
            return result["tasks"] or []
        except KeyError:
            return result

    def get_user_tasks_full(self, company_id, team_id, user_id):
        """
        Retrieve a list of all tasks assigned to a team member \
        (with detail of level at which the task is assigned).

        The user authenticated must have been granted the appropriate
        hiring manager permissions.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :team_id:       Team ID. Use the 'id' value
                          from ``hr.get_team()`` API call.

          :user_id:       User ID

        """
        url = 'tasks/companies/{0}/teams/{1}/users/{2}/tasks/full_list'.format(
            company_id, team_id, user_id)
        result = self.get(url)
        try:
            return result["tasks"] or []
        except KeyError:
            return result

    def _encode_task_codes(self, task_codes):
        if isinstance(task_codes, (list, tuple)):
            return ';'.join(str(c) for c in task_codes)
        else:
            return task_codes

    def get_company_specific_tasks(self, company_id, task_codes):
        """
        Return a specific task record within a company.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :task_codes:    Task codes (must be a list, even of 1 item)

        """
        task_codes = self._encode_task_codes(task_codes)
        url = 'tasks/companies/{0}/tasks/{1}'.format(
            company_id, urllib.quote(task_codes))
        result = self.get(url)
        return result.get("tasks", result)

    def get_team_specific_tasks(self, company_id, team_id, task_codes):
        """
        Return a specific task record within a team.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :team_id:       Team ID. Use the 'id' value
                          from ``hr.get_team()`` API call.

          :task_codes:    Task codes (must be a list, even of 1 item)

        """
        task_codes = self._encode_task_codes(task_codes)
        url = 'tasks/companies/{0}/teams/{1}/tasks/{2}'.format(
            company_id, team_id, urllib.quote(task_codes))
        result = self.get(url)
        try:
            return result["tasks"] or []
        except KeyError:
            return result

    def get_user_specific_tasks(self, company_id, team_id, user_id,
                                task_codes):
        """
        Return a specific task record for a team member.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :team_id:       Team ID. Use the 'id' value
                          from ``hr.get_team()`` API call.

          :user_id:       User ID

          :task_codes:    Task codes (must be a list, even of 1 item)

        """
        task_codes = self._encode_task_codes(task_codes)
        url = 'tasks/companies/{0}/teams/{1}/users/{2}/tasks/{3}'.format(
            company_id, team_id, user_id, urllib.quote(task_codes))
        result = self.get(url)
        try:
            return result["tasks"] or []
        except KeyError:
            return result

    def post_company_task(self, company_id, code, description, url):
        """
        Create a company task.

        The authenticated user needs to have hiring manager privileges.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :code:          Task code

          :description:   Task description

          :url:           Task URL

        """
        url = 'tasks/companies/{0}/tasks'.format(company_id)
        data = {'code': code,
                'description': description,
                'url': url}
        result = self.post(url, data)
        return result

    def post_team_task(self, company_id, team_id, code, description, url):
        """
        Create a team task.

        The authenticated user needs to have hiring manager privileges

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :team_id:       Team ID. Use the 'id' value
                          from ``hr.get_team()`` API call.

          :code:          Task code

          :description:   Task description

          :url:           Task URL

        """
        post_url = 'tasks/companies/{0}/teams/{1}/tasks'.format(
            company_id, team_id)
        data = {'code': code,
                'description': description,
                'url': url}
        result = self.post(post_url, data)
        return result

    def post_user_task(self, company_id, team_id, user_id, code, description,
                       url):
        """
        Create a task assigned to self.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :team_id:       Team ID. Use the 'id' value
                          from ``hr.get_team()`` API call.

          :user_id:       User ID

          :code:          Task code

          :description:   Task description

          :url:           Task URL

        """
        post_url = 'tasks/companies/{0}/teams/{1}/users/{2}/tasks'.format(
            company_id, team_id, user_id)
        data = {'code': code,
                'description': description,
                'url': url}
        result = self.post(post_url, data)
        return result

    def put_company_task(self, company_id, code, description, url):
        """
        Update a company task.

        The authenticated user needs to have hiring manager privileges.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :code:          Task code

          :description:   Task description

          :url:           Task URL

        """
        put_url = 'tasks/companies/{0}/tasks/{1}'.format(
            company_id, urllib.quote(str(code)))
        data = {'code': code,
                'description': description,
                'url': url}
        result = self.put(put_url, data)
        return result

    def put_team_task(self, company_id, team_id, code, description, url):
        """
        Update a team task.

        The authenticated user needs to have hiring manager privileges.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :team_id:       Team ID. Use the 'id' value
                          from ``hr.get_team()`` API call.


          :code:          Task code

          :description:   Task description

          :url:           Task URL

        """
        put_url = 'tasks/companies/{0}/teams/{1}/tasks/{2}'.format(
            company_id, team_id, urllib.quote(str(code)))
        data = {'code': code,
                'description': description,
                'url': url}
        result = self.put(put_url, data)
        return result

    def put_user_task(self, company_id, team_id, user_id, code,
                      description, url):
        """
        Update a task assigned to self.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :team_id:       Team ID. Use the 'id' value
                          from ``hr.get_team()`` API call.

          :user_id:       User ID

          :code:          Task code

          :description:   Task description

          :url:           Task URL

        """
        put_url = 'tasks/companies/{0}/teams/{1}/users/{2}/tasks/{3}'.format(
            company_id, team_id, user_id, urllib.quote(str(code)))
        data = {'code': code,
                'description': description,
                'url': url}
        result = self.put(put_url, data)
        return result

    def delete_company_task(self, company_id, task_codes):
        """
        Delete specific tasks within a company.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :task_codes:    Task codes (must be a list, even of 1 item)

        """
        task_codes = self._encode_task_codes(task_codes)
        data = {'code': task_codes}
        url = 'tasks/companies/{0}/tasks/{1}'.format(
            company_id, urllib.quote(task_codes))
        return self.delete(url, data)

    def delete_team_task(self, company_id, team_id, task_codes):
        """
        Delete specific tasks within a team.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :team_id:       Team ID. Use the 'id' value
                          from ``hr.get_team()`` API call.

          :task_codes:    Task codes (must be a list, even of 1 item)

        """
        task_codes = self._encode_task_codes(task_codes)
        data = {'code': task_codes}
        url = 'tasks/companies/{0}/teams/{1}/tasks/{2}'.format(
            company_id, team_id, urllib.quote(task_codes))
        return self.delete(url, data)

    def delete_user_task(self, company_id, team_id, user_id, task_codes):
        """
        Delete specific tasks assigned to a team member.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :team_id:       Team ID. Use the 'id' value
                          from ``hr.get_team()`` API call.

          :user_id:       User ID

          :task_codes:    Task codes (must be a list, even of 1 item)

        """
        task_codes = self._encode_task_codes(task_codes)
        data = {'code': task_codes}
        url = 'tasks/companies/{0}/teams/{1}/users/{2}/tasks/{3}'.format(
            company_id, team_id, user_id, urllib.quote(task_codes))

        return self.delete(url, data)

    def delete_all_company_tasks(self, company_id):
        """
        Delete all tasks within a company.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

        """
        url = 'tasks/companies/{0}/tasks/all_tasks'.format(company_id)
        return self.delete(url)

    def delete_all_team_tasks(self, company_id, team_id):
        """
        Delete all tasks within a team.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :team_id:       Team ID. Use the 'id' value
                          from ``hr.get_team()`` API call.

        """
        url = 'tasks/companies/{0}/teams/{1}/tasks/all_tasks'.format(
            company_id, team_id)
        return self.delete(url)

    def delete_all_user_tasks(self, company_id, team_id, user_id):
        """
        Delete all tasks assigned to a team member.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :team_id:       Team ID. Use the 'id' value
                          from ``hr.get_team()`` API call.

          :user_id:       User ID

        """
        url = 'tasks/companies/{0}/teams/{1}/users/{2}/tasks/all_tasks'.format(
            company_id, team_id, user_id)
        return self.delete(url)

    def update_batch_tasks(self, company_id, csv_data):
        """
        Batch update tasks using csv file contents.

        This process actually deletes the corresponding tasks and replaces
        them with the newly specified details.

        *Parameters:*
          :company_id:  Company ID. Use the ``parent_team__id`` value
                        from ``hr.get_team()`` API call.

          :csv_data: Task records in csv format but with "<br>"
                     as line separator -
                     "companyid","teamid","userid","taskid","description","url"
                     Example:
                     "acmeinc","","","T1","A Task","http://example.com"<br>
                     "acmeinc","acmeinc:dev","b42","T2","Task 2",""

        """
        data = {'data': csv_data}
        url = 'tasks/companies/{0}/tasks/batch'.format(company_id)

        return self.put(url, data)
