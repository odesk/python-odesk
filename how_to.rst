.. _how_to:


***************
How to
***************

.. note:: Every method is fully documented in the docstring, so you can refer to the :ref:`reference_docs` or directly view help in the interactive console.

To get help on the method use::

    help(client.provider.search_jobs)

or if you use ``IPython`` just add ``?`` symbol at the end of an object/class/method::

    client.provider.search_jobs?

..
.. _authenticate:

Authenticate
-----------------

http://developers.odesk.com/Authentication

To authenticate your web application with the python-odesk, use something similar
to the code below::

    public_key = raw_input('Please enter public key: > ')
    secret_key = raw_input('Please enter secret key: > ')

    #Instantiating a client without an auth token
    client = odesk.Client(public_key, secret_key)

    print "Please to this URL (authorize the app if necessary):"
    print client.auth.get_authorize_url()
    print "After that you should be redirected back to your app URL with " + \
          "additional ?oauth_verifier= parameter"

    verifier = raw_input('Enter oauth_verifier: ')

    oauth_access_token, oauth_access_token_secret = \
        client.auth.get_access_token(verifier)

    # Instantiating a new client, now with a token.
    # Not strictly necessary here (could just set `client.oauth_access_token`
    # and `client.oauth_access_token_secret`), but typical for web apps,
    # which wouldn't probably keep client instances between requests
    client = odesk.Client(public_key, secret_key,
                          oauth_access_token=oauth_access_token,
                          oauth_access_token_secret=oauth_access_token_secret)

..
.. _provider_information:

Provider's information
--------------------------

http://developers.odesk.com/Provider-Profile


.. currentmodule:: odesk.routers.provider.Provider

To get information about provider, use following methods (click the link to see detailed description of parameters):

:py:meth:`client.provider.get_provider<get_provider>`

:py:meth:`client.provider.get_provider_brief<get_provider_brief>`


Search Providers
----------------

.. currentmodule:: odesk.routers.provider.Provider_V2

To search provider(http://developers.odesk.com/search-providers) by the query string, use:

:py:meth:`client.provider_v2.search_providers<search_providers>`

Search Jobs
-----------

To search jobs(http://developers.odesk.com/search-jobs) by the query string, use:

:py:meth:`client.provider_v2.search_jobs<search_jobs>`


.. _metadata_information:

Metadata information
------------------------

.. currentmodule:: odesk.routers.provider.Provider

To get information about available categories, skills, regions and tests use:

:py:meth:`client.provider.get_categories_metadata<get_categories_metadata>`

:py:meth:`client.provider.get_skills_metadata<get_skills_metadata>`

:py:meth:`client.provider.get_regions_metadata<get_regions_metadata>`

:py:meth:`client.provider.get_tests_metadata<get_tests_metadata>`


..
.. _hiring:

Hiring
------

.. currentmodule:: odesk.routers.hr.HR

oDesk Hiring API http://developers.odesk.com/w/page/23879811/Hiring allows to do such tasks as:

* Create new job posting :py:meth:`client.hr.post_job<post_job>`

* Update existing job post :py:meth:`client.hr.update_job<update_job>`

* View existing jobs :py:meth:`client.hr.get_jobs<get_jobs>`
.. currentmodule:: odesk.routers.hr.HR_V1
* Invite to interview :py:meth:`client.hr_v1.invite_to_interview<invite_to_interview>`
.. currentmodule:: odesk.routers.hr.HR
* Make an offer :py:meth:`client.hr.post_offer<post_offer>`

* View active engagements :py:meth:`client.hr.get_engagements<get_engagements>`

* Pay a bonus to the contractor :py:meth:`client.hr.post_team_adjustment<post_team_adjustment>`

* End the contract with provider :py:meth:`client.hr.end_contract<end_contract>`


..
.. _work_with_jobs:

Work with jobs
----------------------

http://developers.odesk.com/w/page/49065901/Job%20Profile

.. currentmodule:: odesk.routers.job

To work with jobs you should use :py:class:`client.job<Job>` wrapper::

    tasks = client.job.get_job_profile(job key)

Where:

* job_key - The job key or a list of keys, separated by ``";"``, number of keys per request is limited by 20. You can access profile by job reference number, in that case you can't specify a list of jobs, only one profile per request is available.

..
.. _team_information:

Team's information
----------------------

http://developers.odesk.com/Team-API

.. currentmodule:: odesk.routers.team.Team_V2

After authentication, you can get teams' information from client instance you have:

:py:meth:`client.team_v2.get_teamrooms<get_teamrooms>`

To get snapshots:

:py:meth:`client.team_v2.get_snapshots<get_snapshots>`

.. currentmodule:: odesk.routers.team.Team

To get user's workdiaries inside the team:

:py:meth:`client.team.get_workdiaries<get_workdiaries>`


..
.. _get_messages:

Trays and messages
-----------------------

http://developers.odesk.com/Message-Center-API

.. currentmodule:: odesk.routers.mc.MC

Get user's trays (if user not provided, authenticated user will be taken):

:py:meth:`client.mc.get_trays<get_trays>`

Get content of the tray:

:py:meth:`client.mc.get_tray_content<get_tray_content>`

Get content of the thread:

:py:meth:`client.mc.get_thread_content<get_thread_content>`


..
.. _send_message:

Send message
----------------------

http://developers.odesk.com/Message-Center-API

To send message:

:py:meth:`client.mc.post_message<post_message>`


..
.. _get_timereports:

Get timereports
----------------------

.. currentmodule:: odesk.routers.timereport.TimeReport

http://developers.odesk.com/Time-Reports-API

To get timereports, use, based on the level of the timereports you need:

:py:meth:`client.timereport.get_provider_report<get_provider_report>`

:py:meth:`timereport.get_company_report<get_agency_report>`

:py:meth:`timereport.get_agency_report<get_agency_report>`

Below is an example how to construct a GDS query::

    client.timereport.get_provider_report('user1',
           odesk.utils.Query(select=odesk.utils.Query.DEFAULT_TIMEREPORT_FIELDS,
                        where=(odesk.utils.Q('worked_on') <= date.today()) &\
                                (odesk.utils.Q('worked_on') > '2010-05-01')))


    client.timereport.get_provider_report('user1',
           odesk.utils.Query(select=odesk.utils.Query.DEFAULT_TIMEREPORT_FIELDS,
                        where=(odesk.utils.Q('worked_on') <= date.today()) &\
                                (odesk.utils.Q('worked_on') > '2010-05-01')), hours=True)

    client.timereport.get_agency_report('company1', 'agency1',
           odesk.utils.Query(select=odesk.utils.Query.DEFAULT_TIMEREPORT_FIELDS,
                        where=(odesk.utils.Q('worked_on') <= date.today()) &\
                                (odesk.utils.Q('worked_on') > '2010-05-01')), hours=True)


..
.. _get_finreports:

Get finreports
----------------------

.. currentmodule:: odesk.routers.finreport

Financial reports are also using GDS queries.

Please see :py:class:`Finreports` wrapper

..
.. _work_with_tasks:

Work with tasks
----------------------

http://developers.odesk.com/oTasks-API

.. currentmodule:: odesk.routers.task

To work with tasks you should use :py:class:`client.otask<Task>` wrapper::

    tasks = client.otask.get_company_tasks('company_id')

.. currentmodule:: odesk.routers.task.Task

Methods to get tasks:

:py:meth:`client.task.get_team_tasks<get_team_tasks>`

:py:meth:`client.task.get_user_tasks<get_user_tasks>`

:py:meth:`client.task.get_company_tasks_full<get_company_tasks_full>`

:py:meth:`client.task.get_team_tasks_full<get_team_tasks_full>`

:py:meth:`client.task.get_user_tasks_full<get_user_tasks_full>`

:py:meth:`client.task.get_company_specific_tasks<get_company_specific_tasks>`

:py:meth:`client.task.get_team_specific_tasks<get_team_specific_tasks>`

:py:meth:`client.task.get_user_specific_tasks<get_user_specific_tasks>`

Create and update tasks:

:py:meth:`client.task.post_company_task<post_company_task>`

:py:meth:`client.task.post_team_task<post_team_task>`

:py:meth:`client.task.post_user_task<post_user_task>`

:py:meth:`client.task.put_company_task<put_company_task>`

:py:meth:`client.task.put_team_task<put_team_task>`

:py:meth:`client.task.put_user_task<put_user_task>`

Delete tasks:

:py:meth:`client.task.delete_company_task<delete_company_task>`

:py:meth:`client.task.delete_team_task<delete_team_task>`

:py:meth:`client.task.delete_user_task<delete_user_task>`

:py:meth:`client.task.delete_all_company_tasks<delete_all_company_tasks>`

:py:meth:`client.task.delete_all_team_tasks<delete_all_team_tasks>`

:py:meth:`client.task.delete_all_user_tasks<delete_all_user_tasks>`

Batch update of tasks:

:py:meth:`client.task.update_batch_tasks(company_id, csv_data)<update_batch_tasks>`

Where csv_data - is the raw csv data for tasks to be updated. Example::

    "acmeinc","","","ABC","Project ABC","https://www.acmeinc.com/project/abc"<br>"acmeinc","acmeinc:dev","b42","123","Task 123","https://www.acmeinc.com/task/123"
