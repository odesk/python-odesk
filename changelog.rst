.. _changelog:


***************
Changelog
***************

.. _0.5.6:

Version 0.5.6
-------------
* Added new API call - :py:meth:`List categories (v2) <odesk.routers.provider.Provider_V2.get_categories_metadata>`.
* Added new API call - :py:meth:`Get Work Diary by Contract <odesk.routers.team.Team_V2.get_workdiaries_by_contract>`.
* Recent changes from API Changelog - Wednesday, 2015-01-12
* Recent changes from API Changelog - Wednesday, 2014-12-03
* Recent changes from API Changelog - Friday, 2014-11-21
* Recent changes from API Changelog - Friday, 2014-10-31

.. _0.5.5:

Version 0.5.5
-------------
* Added new API call - :py:meth:`Create a new Milestone <odesk.routers.hr.HR_V3.create_milestone>`.
* Added new API call - :py:meth:`Edit the Milestone <odesk.routers.hr.HR_V3.edit_milestone>`.
* Added new API call - :py:meth:`Approve the Milestone <odesk.routers.hr.HR_V3.approve_milestone>`.
* Added new API call - :py:meth:`Activate the Milestone <odesk.routers.hr.HR_V3.activate_milestone>`.
* Added new API call - :py:meth:`Delete the Milestone <odesk.routers.hr.HR_V3.delete_milestone>`.
* Added new API call - :py:meth:`Submit for Approval <odesk.routers.hr.HR_V3.request_submission_approval>`.
* Added new API call - :py:meth:`Approve the Submission <odesk.routers.hr.HR_V3.approve_submission>`.
* Added new API call - :py:meth:`Reject the Submission <odesk.routers.hr.HR_V3.reject_submission>`.
* Added new API call - :py:meth:`Get all Submissions for the Milestone <odesk.routers.hr.HR_V3.get_milestone_submissions>`.
* Added new API call - :py:meth:`Get Active Milestone for the Contract <odesk.routers.hr.HR_V3.get_active_milestone>`.

* ``end_date`` parameter in :py:meth:`Post Job <odesk.routers.hr.HR.post_job>` ad :py:meth:`Update Job <odesk.routers.hr.HR.update_job>` is deprecated, keyword argument still remains for backwards compatibility
  and will be removed in future releases.

.. _0.5.4:

Version 0.5.4
-------------
* Added new API call - :py:meth:`Suspend Contract <odesk.routers.hr.HR.suspend_contract>`.
* Added new API call - :py:meth:`Restart Contract <odesk.routers.hr.HR.restart_contract>`.
* :py:meth:`Archive <odesk.routers.task.Task.archive_team_task>`/:py:meth:`unarchive <odesk.routers.task.Task.unarchive_team_task>` activities calls now support a list of codes.

.. _0.5.3:

Version 0.5.3
-------------
* New API calls added:
    1. Added :py:meth:`List activities for specific engagement<odesk.routers.task.Task_V2.list_engagement_activities>` via ``task_v2`` router.
    2. Added :py:meth:`Reasons metadata<odesk.routers.provider.Provider.get_reasons_metadata>` call.
    3. Added :py:class:`Offers router<odesk.routers.offers.Offers>` with handy number of calls for managing offers as a client and as a freelancer.
    4. Added :py:class:`HR_V3 router<odesk.routers.hr.HR_V3>` with a number of calls for getting job applications  as a client and as a freelancer.
    5. Added :py:meth:`List threads by context <odesk.routers.mc.MC.get_thread_by_context>` call.
* Removed mistakenly documented by oDesk but not working API call for getting team adjustments.

.. _0.5.2:

Version 0.5.2
-------------
* Fixed engagements API call, so that you can call
  ``client.hr.get_engagements()`` without any parameter
  to get all engagements for authorized user.
* oTask API strongly reworked, from now Task Codes are
  renamed to Activities and it's behavior is changed:

    1. Activity now is assigned to the engagement ID.
       It will appear it user's oDesk Team Client only if
       it was assigned to the user's engagement.
    2. You cannot delete activity. You can archive it
       and unarchive if necessary.
    3. Activities are created on the team level,
       you can create a company level activities by
       passing ``team_id`` that is equal to ``company_id``
       (which is ``parent__team_id``). There's a methods
       for this already, please see the reference documentation.
       Note that archived activity has empty engagements list,
       so if you decide to unarchive an activity, you need to
       do an extra update call to assign the activity to someone.
    4. When creating/updating activities you can pass optional
       ``engagements`` parameter, that should be a list of engagements
       that will be assigned to the Activity. Otherwise the activity
       won't be assigned to anyone. If you want to assign created/updated
       activity to all engagements in the company, you can set
       the ``all_in_company`` parameter.
    5. ``update_batch_tasks`` call is marked as experimental,
       use it on your own risk. It will be reworked in future.

.. _0.5.1:

Version 0.5.1
-------------
* Fixed bug preventing update (``PUT`` method) for oTask codes that
  contained non-urlsafe characters, e.g. "space", "colon", etc.

.. _0.5:

Version 0.5
-----------------
*October 2013*

Backwards incompatibility changes:

* Old key-based authorization is completely removed, now the only way
  to authorize is oAuth 1.0
* ``odesk.Client`` class doesn't support ``auth`` keyword argument any more,
  as now there's only one way of doing authorization
* Introduced V2 API calls for
  :py:meth:`Search Providers<odesk.routers.provider.Provider_V2.search_providers>` and
  :py:meth:`Search Jobs<odesk.routers.provider.Provider_V2.search_jobs>`.
  V1 API calls still work but to the end of 2013 will be switched off.
  So we greatly encourage you to use V2 API calls.
* ``examples/`` directory of the repository is updated with new examples for
  web and desktop application

Improvements:

* Clean up API to be consistent with official oDesk API documentation
* Now we use ``urllib3`` and all Http exceptions returned by API have
  meaningful messages
* Real PUT and DELETE json calls
* Some parts of API are fixed with to work correctly. Please refer to the
  method's docstring to see comprehensive description

*Nov 2012*

* Add Metadata Api
* Fixed job posting issue
* Add advanced logging


.. _0.4:

Version 0.4
-----------------
*May 2011*

* *Incompatibility with previous release* Changed name of the otask router to the task
* *Incompatibility with previous release* Chaged name of the oticket router to the ticket ??
* *Incompatibility with previous release* Changed name of the time_report router to the timereport
* *Incompatibility with previous release* Changed name of the finreports router to the finreport
* *Incompatibility with previous release* "from odesk import \*" now import only: "get_version", "Client", "utils"
* All routers moved from the __init__.py to the own files in the routers dir.
* All helper classes moved to own modules
* Added logging inside exceptions
* Added possiblity to switch off unused routers inside client class
* Added oconomy, finance routers
* Added oDesk oAuth support

.. _0.2:

Version 0.2
-----------------
*October 2010*

* All helpers classes moved to the utils.py, added Table helper class
* *Incompatibility with previous release* Changed names of the methods' params to reflect real oDesk params - e.g. company_reference vs company name

.. _0.1.2:

Version 0.1.2
-----------------
*29 September 2010*

Bug fix release

* Fixed check_token method
* Fixed KeyError on empty workdiaries

.. _0.1.1:

Version 0.1.1
-----------------
*15 July 2010*

Bug fix release

* Fixed HR2.get_user_role(user_id=None, team_id=None, sub_teams=False) method to correctly get user roles when both user reference and team reference were submitted - previously only one of them was used in the request
* Documentation fixes

.. _0.1:

Version 0.1
-----------------
*08 July 2010*

First public release
