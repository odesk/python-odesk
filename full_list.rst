.. _full_list:


********************************
Full list of classes and methods
********************************

..
.. _package:

Package structure
--------------------

* __init__.py
* auth.py
* exceptions.py
* http.py
* namespace.py
* oauth.py
* utils.py
* routers

   * __init__.py
   * finance.py
   * finreport.py
   * hr.py
   * job.py
   * mc.py
   * provider.py
   * task.py
   * team.py
   * ticket.py
   * timereport.py
   * url.py

* tests.py

.. __init__:

__init__.py
------------------------------------

* class BaseClient(object)

A basic HTTP client which supports signing of requests as well as de-serializing of responses.

* class Client(BaseClient)

 * def __init__(self, public_key, secret_key, api_token=None,
                format='json', auth='simple', finance=True, finreport=True,
                hr=True, mc=True, oconomy=True, provider=True,
                task=True, team=True, ticket=True, timereport=True, url=True)

 * Variables available inside Client:

  * public_key
  * secret_key
  * api_token
  * format

 * Routers inside Client:

  * auth
  * finance
  * finreport
  * hr
  * mc
  * oconomy
  * provider
  * task
  * team
  * ticket
  * timereport
  * url

You can disable any of router except auth, by specifing router_name=False during Client initialization, e.g:

   odesk_client = odesk.Client(public_key, secret_key, ticket=False)

..
.. _auth:

auth.py
-----------------
* Auth(Namespace)

 * auth_url
 * get_frob
 * get_token
 * check_token

..
.. _exceptions:

exceptions.py
---------------------------

* class BaseException(Exception)
* class HTTP400BadRequestError(urllib2.HTTPError, BaseException)
* class HTTP401UnauthorizedError(urllib2.HTTPError, BaseException)
* class HTTP403ForbiddenError(urllib2.HTTPError, BaseException)
* class HTTP404NotFoundError(urllib2.HTTPError, BaseException)
* class InvalidConfiguredException(BaseException)
* class APINotImplementedException(BaseException)
* class AuthenticationError(BaseException)
* class NotAuthenticatedError(BaseException)

..
.. _http:

http.py
-----------------
* def raise_http_error(e)

Raise appropriate exception depending on the code returned by urllib2

* class HttpRequest(urllib2.Request)

A hack around Request class that allows to specify HTTP method explicitly


.. _namespaces:

namespaces.py
--------------------------

* class Namespace

 * base_url = 'https://www.odesk.com/api/'
 * api_url = None
 * version = 1
 * #Proxied client's methods
 * get(self, url, data={})
 * post(self, url, data={}):
 * put(self, url, data={}):
 * delete(self, url, data={}):

* class GdsNamespace(Namespace)

 * base_url = 'https://www.odesk.com/gds/'
 * #methods
 * urlopen(self, url, data={}, method='GET')
 * read(self, url, data={}, method='GET')
 * get(self, url, data={})

* class NonAuthGdsNamespace(GdsNamespace)

 * #methods
 * urlopen(self, url, data={}, method='GET')


..
.. _oauth:

oauth.py
-----------------

* class OAuth(Namespace)

 * api_url = 'auth/'
 * version = 1
 * request_token_url = 'https://www.odesk.com/api/auth/v1/oauth/token/request'
 * authorize_url = 'https://www.odesk.com/services/api/auth'
 * access_token_url = 'https://www.odesk.com/api/auth/v1/oauth/token/access'
 * #methods
 * urlencode(self, url, key, secret, data={}, method='GET')
        """
        Converts a mapping object to signed url query
        """
 * get_oauth_consumer(self)
        """
        Returns OAuth consumer object
        """
 * get_request_token(self)
        """
        Returns request token and request token secret
        """
 * get_authorize_url(self, callback_url=None):
        """
        Returns authentication URL to be used in a browser
        """
 * get_access_token(self, verifier):
        """
        Returns access token and access token secret
        """



.. _routers:

routers/
---------------------

* Finances(Namespace) - routers/finance.py

* Finreports(GdsNamespace) - routers/finreport.py

 * get_provider_billings(self, provider_id, query)
 * get_provider_teams_billings(self, provider_team_id, query)
 * get_provider_companies_billings(self, provider_company_id, query)
 * get_provider_earnings(self, provider_id, query)
 * get_provider_teams_earnings(self, provider_team_id, query)
 * get_provider_companies_earnings(self, provider_company_id, query)
 * get_buyer_teams_billings(self, buyer_team_id, query)
 * get_buyer_companies_billings(self, buyer_company_id, query)
 * get_buyer_teams_earnings(self, buyer_team_id, query)
 * get_buyer_companies_earnings(self, buyer_company_id, query)
 * get_financial_entities(self, accounting_id, query)
 * get_financial_entities_provider(self, provider_id, query)

* Job(Namespace) - routers/job.py

 * get_job_profile(self, job_key)

* HR(Namespace) - routers/hr.py

 * get_user(self, user_id)
 * get_companies(self)
 * get_company(self, company_id)
 * get_company_teams(self, company_id)
 * get_company_tasks(self, company_id) - Not implemented in API
 * get_company_users(self, company_id,  active=True)
 * get_teams(self)
 * get_team(self, team_id, include_users=False)
 * get_team_tasks(self, team_id) - Not implemented in API
 * get_team_users(self, team_id, active=True)
 * post_team_adjustment(self, team_id, engagement_id, amount, comments, notes)
 * get_tasks(self) - Not implemented in API
 * get_user_role(self, user_id=None, team_id=None, sub_teams=False)
 * get_jobs(self)
 * get_job(self, job_id)
 * get_offers(self)
 * get_offer(self, offer_id)
 * get_engagements(self)
 * get_engagement(self, engagement_id)

* HR_V1(Namespace) - routers/hr.py

  * invite_to_interview(job_id, cover, profile_key=None, provider_reference=None)

* MC(Namespace) - routers/mc.py

 * get_trays(self, username=None, paging_offset=0, paging_count=20)
 * get_tray_content(self, username, tray, paging_offset=0, paging_count=20)
 * get_thread_content(self, username, thread_id, paging_offset=0, paging_count=20)
 * put_threads_read(self, username, thread_ids)
 * put_threads_unread(self, username, thread_ids)
 * put_threads_starred(self, username, thread_ids)
 * put_threads_unstarred(self, username, thread_ids)
 * put_threads_deleted(self, username, thread_ids)
 * put_threads_undeleted(self, username, thread_ids)
 * post_message(self, username, recipients, subject, body, thread_id=None)

* Provider (Namespace) - routers/provider.py

 * get_provider(self, provider_ciphertext)
 * get_provider_brief(self, provider_ciphertext)
 * get_providers(self, data=None, page_offset=0, page_size=20, order_by=None)
 * get_jobs(self, data=None, page_offset=0, page_size=20, order_by=None)
 * get_skills(self, provider_ciphertext)
 * add_skill(self, provider_ciphertext, data)
 * update_skill(self, provider_ciphertext, skill_id, data)
 * delete_skill(self, provider_ciphertext, skill_id)
 * get_quickinfo(self, provider_ciphertext)
 * update_quickinfo(self, provider_ciphertext, data)
 * get_affiliates(self, affiliate_key)
 * get_categories_metadata(self)
 * get_skills_metadata(self)
 * get_regions_metadata(self)
 * get_tests_metadata(self)

* Task(Namespace) - routers/task.py

 * get_company_tasks(self, company_id)
 * get_team_tasks(self, company_id, team_id)
 * get_user_tasks(self, company_id, team_id, user_id)
 * get_company_tasks_full(self, company_id)
 * get_team_tasks_full(self, company_id, team_id)
 * get_user_tasks_full(self, company_id, team_id, user_id)
 * get_company_specific_tasks(self, company_id, task_codes)
 * get_team_specific_tasks(self, company_id, team_id, task_codes)
 * get_user_specific_tasks(self, company_id, team_id, user_id, task_codes)
 * post_company_task(self, company_id, code, description, url)
 * post_team_task(self, company_id, team_id, code, description, url)
 * post_user_task(self, company_id, team_id, user_id, code, description, url)
 * put_company_task(self, company_id, code, description, url)
 * put_team_task(self, company_id, team_id, code, description, url)
 * put_user_task(self, company_id, team_id, user_id, code, description, url)
 * delete_company_task(self, company_id, task_codes)
 * delete_team_task(self, company_id, team_id, task_codes)
 * delete_user_task(self, company_id, team_id, user_id, task_codes)
 * delete_all_company_tasks(self, company_id)
 * delete_all_team_tasks(self, company_id, team_id)
 * delete_all_user_tasks(self, company_id, team_id, user_id)
 * update_batch_tasks(self, company_id, csv_data)

* Team(Namespace) - routers/team.py

 * get_teamrooms(self)
 * get_snapshots(self, team_id, online='now')
 * get_workdiaries(self, team_id, username, date=None)

* Ticket(Namespace) - routers/ticket.py

* Timereport(GdsNamespace) - routers/timereport.py

 * get_provider_report(self, provider_id, query, hours=False)
 * get_company_report(self, company_id, query, hours=False)
 * get_agency_report(self, company_id, agency_id, query, hours=False)
 * query is the odesk.Query object

* Url(Namespace) - routers/url.py


.. _utils:

utils.py
---------------------
* Q(object)

 * Simple query constructor
 * Example of usage::

    odesk.Q('worked_on') <= date.today()


* Query(object)

 * Simple query
 * DEFAULT_TIMEREPORT_FIELDS = ['worked_on', 'team_id', 'team_name', 'task', 'memo','hours',]
 * DEFAULT_FINREPORT_FIELDS = ['reference', 'date', 'buyer_company__id', 'buyer_company_name', 'buyer_team__id', 'buyer_team_name', 'provider_company__id', 'provider_company_name', 'provider_team__id', 'provider_team_name', 'provider__id', 'provider_name', 'type', 'subtype', 'amount']
 * __init__(self, select, where=None, order_by=None)
 * __str__(self)
 * Examples of usage::

    odesk.Query(select=odesk.Query.DEFAULT_TIMEREPORT_FIELDS, where=(odesk.Q('worked_on') <= date.today()) & (odesk.Q('worked_on') > '2010-05-01'))
    odesk.Query(select=['date', 'type', 'amount'], where=(odesk.Q('date') <= date.today()))

* Table(object)
