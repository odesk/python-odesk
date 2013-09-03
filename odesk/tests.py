# -*- coding: utf-8 -*-
"""
Python bindings to odesk API
python-odesk version 0.4
(C) 2010 oDesk
"""
from odesk import Client, BaseClient, utils, get_version, signed_urlencode
from odesk.exceptions import *
from odesk.namespaces import *
from odesk.auth import Auth
from odesk.oauth import OAuth
from odesk.routers.team import Team
from odesk.http import ODESK_ERROR_CODE, ODESK_ERROR_MESSAGE

from mock import Mock, patch
import urlparse
import urllib2
import urllib3
import httplib

try:
    import json
except ImportError:
    import simplejson as json


class MicroMock(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def test_signed_urlencode():
    secret_data = {
    'some$ecret': {'query': {},
                   'result':
                   'api_sig=5da1f8922171fbeffff953b773bcdc7f'},
    'some$ecret': {'query': {'spam': 42, 'foo': 'bar'},
                   'result':
                   'api_sig=11b1fc2e6555297bdc144aed0a5e641c&foo=bar&spam=42'},
    'som[&]234e$ecret': {'query': {'spam': 42, 'foo': 'bar'},
                   'result':
                   'api_sig=ac0e1b26f401dd4a5ccbaf7f4ea86b2f&foo=bar&spam=42'},
               }
    for key in secret_data.keys():
        result = signed_urlencode(key, secret_data[key]['query'])
        assert secret_data[key]['result'] == result, \
            " {0} returned and should be {1}".format(result,
                                                     secret_data[key]['result'])


def test_base_client():
    public_key = 'public'
    secret_key = 'secret'

    bc = BaseClient(public_key, secret_key)

    #test urlencode
    urlresult = bc.urlencode({'spam': 42, 'foo': 'bar'})
    encodedkey = 'api_sig=8a0da3cab1dbf7451f38fb5f5aec129c&api_key=public&foo=bar&spam=42'
    assert urlresult == encodedkey, urlresult

sample_json_dict = {u'glossary':
                    {u'GlossDiv':
                     {u'GlossList':
                      {u'GlossEntry':
                       {u'GlossDef':
                        {u'GlossSeeAlso': [u'GML', u'XML'],
                         u'para': u'A meta-markup language'},
                         u'GlossSee': u'markup',
                         u'Acronym': u'SGML',
                         u'GlossTerm': u'Standard Generalized Markup Language',
                         u'Abbrev': u'ISO 8879:1986',
                         u'SortAs': u'SGML',
                         u'ID': u'SGML'}},
                         u'title': u'S'},
                         u'title': u'example glossary'}}


def patched_urlopen(*args, **kwargs):
    return MicroMock(data=json.dumps(sample_json_dict), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen)
def test_base_client_urlopen():
    public_key = 'public'
    secret_key = 'secret'

    bc = BaseClient(public_key, secret_key)

    #test urlopen
    data = [{'url': 'http://test.url',
             'data': {'foo': 'bar'},
             'method': 'GET',
             'result_data': None,
             'result_url': 'http://test.url?api_sig=ddbf4b10a47ca8300554441dc7c9042b&api_key=public&foo=bar',
             'result_method': 'GET'},
             {'url': 'http://test.url',
             'data': {},
             'method': 'POST',
             'result_data': 'api_sig=ba343f176db8166c4b7e88911e7e46ec&api_key=public',
             'result_url': 'http://test.url',
             'result_method': 'POST'},
             {'url': 'http://test.url',
             'data': {},
             'method': 'PUT',
             'result_data': 'api_sig=52cbaea073a5d47abdffc7fc8ccd839b&api_key=public&http_method=put',
             'result_url': 'http://test.url',
             'result_method': 'POST'},
             {'url': 'http://test.url',
             'data': {},
             'method': 'DELETE',
             'result_data': 'api_sig=8621f072b1492fbd164d808307ba72b9&api_key=public&http_method=delete',
             'result_url': 'http://test.url',
             'result_method': 'POST'},
             ]

    result_json = json.dumps(sample_json_dict)

    for params in data:
        result = bc.urlopen(url=params['url'],
                            data=params['data'],
                            method=params['method'])
        assert result.data == result_json, (result.data, result_json)


def patched_urlopen_error(method, url, code=httplib.BAD_REQUEST,
                          message=None, **kwargs):
    getheaders = Mock()
    getheaders.return_value = {ODESK_ERROR_CODE: code,
                               ODESK_ERROR_MESSAGE: message}
    return MicroMock(data='', getheaders=getheaders, status=code)


def patched_urlopen_400(self, method, url, **kwargs):
    return patched_urlopen_error(
        method, url, code=httplib.BAD_REQUEST,
        message='Limit exceeded', **kwargs)


def patched_urlopen_401(self, method, url, **kwargs):
    return patched_urlopen_error(
        method, url, code=httplib.UNAUTHORIZED,
        message='Not authorized', **kwargs)


def patched_urlopen_403(self, method, url, **kwargs):
    return patched_urlopen_error(
        method, url, code=httplib.FORBIDDEN,
        message='Forbidden', **kwargs)


def patched_urlopen_404(self, method, url, **kwargs):
    return patched_urlopen_error(
        method, url, code=httplib.NOT_FOUND,
        message='Not found', **kwargs)


def patched_urlopen_500(self, method, url, **kwargs):
    return patched_urlopen_error(
        method, url, code=httplib.INTERNAL_SERVER_ERROR,
        message='Internal server error', **kwargs)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_400)
def base_client_read_400(bc, url):
    return bc.read(url)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_401)
def base_client_read_401(bc, url):
    return bc.read(url)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_403)
def base_client_read_403(bc, url):
    return bc.read(url)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_404)
def base_client_read_404(bc, url):
    return bc.read(url)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_500)
def base_client_read_500(bc, url):
    return bc.read(url)


@patch('urllib3.PoolManager.urlopen', patched_urlopen)
def test_base_client_read():
    """
    test cases:
      method default (get) - other we already tested
      format json|yaml ( should produce error)
      codes 200|400|401|403|404|500
    """
    public_key = 'public'
    secret_key = 'secret'

    bc = BaseClient(public_key, secret_key)
    test_url = 'http://test.url'

    #produce error on format other then json
    class NotJsonException(Exception):
        pass

    try:
        bc.read(url=test_url, format='yaml')
        raise NotJsonException()
    except NotJsonException, e:
        assert 0, "BaseClient.read() doesn't produce error on yaml format"
    except:
        pass

    #test get, all ok
    result = bc.read(url=test_url)
    assert result == sample_json_dict, result

    #test get, 400 error
    try:
        result = base_client_read_400(bc=bc, url=test_url)
    except HTTP400BadRequestError, e:
        pass
    except Exception, e:
        assert 0, "Incorrect exception raised for 400 code: " + str(e)

    #test get, 401 error
    try:
        result = base_client_read_401(bc=bc, url=test_url)
    except HTTP401UnauthorizedError, e:
        pass
    except Exception, e:
        assert 0, "Incorrect exception raised for 401 code: " + str(e)

    #test get, 403 error
    try:
        result = base_client_read_403(bc=bc, url=test_url)
    except HTTP403ForbiddenError, e:
        pass
    except Exception, e:
        assert 0, "Incorrect exception raised for 403 code: " + str(e)

    #test get, 404 error
    try:
        result = base_client_read_404(bc=bc, url=test_url)
    except HTTP404NotFoundError, e:
        pass
    except Exception, e:
        assert 0, "Incorrect exception raised for 404 code: " + str(e)

    #test get, 500 error
    try:
        result = base_client_read_500(bc=bc, url=test_url)
    except urllib2.HTTPError, e:
        if e.code == httplib.INTERNAL_SERVER_ERROR:
            pass
        else:
            assert 0, "Incorrect exception raised for 500 code: " + str(e)
    except Exception, e:
        assert 0, "Incorrect exception raised for 500 code: " + str(e)


def get_client():
    public_key = 'public'
    secret_key = 'secret'
    api_token = 'some_token'
    return Client(public_key, secret_key, api_token)


@patch('urllib3.PoolManager.urlopen', patched_urlopen)
def test_client():
    c = get_client()
    test_url = "http://test.url"

    result = c.get(test_url)
    assert result == sample_json_dict, result

    result = c.post(test_url)
    assert result == sample_json_dict, result

    result = c.put(test_url)
    assert result == sample_json_dict, result

    result = c.delete(test_url)
    assert result == sample_json_dict, result


@patch('urllib3.PoolManager.urlopen', patched_urlopen)
def test_namespace():
    ns = Namespace(get_client())
    test_url = "http://test.url"

    #test full_url
    full_url = ns.full_url('test')
    assert full_url == 'https://www.odesk.com/api/Nonev1/test', full_url

    result = ns.get(test_url)
    assert result == sample_json_dict, result

    result = ns.post(test_url)
    assert result == sample_json_dict, result

    result = ns.put(test_url)
    assert result == sample_json_dict, result

    result = ns.delete(test_url)
    assert result == sample_json_dict, result


def setup_auth():
    return Auth(get_client())


def test_auth():

    au = setup_auth()

    #test full_url
    full_url = au.full_url('test')
    assert full_url == 'https://www.odesk.com/api/auth/v1/test', full_url

    auth_url = au.auth_url('test')
    auth_url_result = 'https://www.odesk.com/services/api/auth/?frob=test&api_key=public&api_sig=42b7f18cbc5c16b1f037dbad241f2a6b&api_token=some_token'
    assert 'frob=test' in auth_url, auth_url
    assert 'api_key=public' in auth_url, auth_url
    assert 'api_sig=42b7f18cbc5c16b1f037dbad241f2a6b' in auth_url, auth_url


frob_dict = {'frob': 'test'}


def patched_urlopen_frob(*args, **kwargs):
    return MicroMock(data=json.dumps(frob_dict), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_frob)
def test_auth_get_frob():
    #test get_frob
    au = setup_auth()
    assert au.get_frob() == frob_dict['frob']


token_dict = {'token': 'testtoken', 'auth_user': 'test_auth_user'}


def patched_urlopen_token(*args, **kwargs):
    return MicroMock(data=json.dumps(token_dict), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_token)
def test_auth_get_token():
    #test get_frob
    au = setup_auth()
    token, auth_user = au.get_token('test_token')
    assert token == token_dict['token'], token
    assert auth_user == token_dict['auth_user'], auth_user


@patch('urllib3.PoolManager.urlopen', patched_urlopen_token)
def test_check_token_true():
    #check if ok
    au = setup_auth()
    try:
        au.check_token()
    except:
        pass
    else:
        assert "Not Raised"


@patch('urllib3.PoolManager.urlopen', patched_urlopen_token)
def test_revoke_token_true():
    #check if ok
    au = setup_auth()
    assert au.revoke_token(), au.revoke_token()


@patch('urllib3.PoolManager.urlopen', patched_urlopen_403)
def test_check_token_false():
    #check if denied
    au = setup_auth()
    try:
        au.check_token()
    except:
        pass
    else:
        assert "Not Raised"


teamrooms_dict = {'teamrooms':
                  {'teamroom':
                   {u'team_ref': u'1',
                    u'name': u'oDesk',
                    u'recno': u'1',
                    u'parent_team_ref': u'1',
                    u'company_name': u'oDesk',
                    u'company_recno': u'1',
                    u'teamroom_api': u'/api/team/v1/teamrooms/odesk:some.json',
                    u'id': u'odesk:some'}},
                  'teamroom': {'snapshot': 'test snapshot'},
                  'snapshots': {'user': 'test', 'snapshot': 'test'},
                  'snapshot': {'status': 'private'}
                 }


def patched_urlopen_teamrooms(*args, **kwargs):
    return MicroMock(data=json.dumps(teamrooms_dict), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_teamrooms)
def test_team():
    te = Team(get_client())

    #test full_url
    full_url = te.full_url('test')
    assert full_url == 'https://www.odesk.com/api/team/v1/test', full_url

    #test get_teamrooms
    assert te.get_teamrooms() == [teamrooms_dict['teamrooms']['teamroom']], \
         te.get_teamrooms()

    #test get_snapshots
    assert te.get_snapshots(1) == [teamrooms_dict['teamroom']['snapshot']], \
         te.get_snapshots(1)

    #test get_snapshot
    assert te.get_snapshot(1, 1) == teamrooms_dict['snapshot'], te.get_snapshot(1, 1)

    #test update_snapshot
    assert te.update_snapshot(1, 1, memo='memo') == teamrooms_dict, te.update_snapshot(1, 1, memo='memo')

    #test update_snapshot
    assert te.delete_snapshot(1, 1) == teamrooms_dict, te.delete_snapshot(1, 1)

    #test get_workdiaries
    assert te.get_workdiaries(1, 1, 1) == (teamrooms_dict['snapshots']['user'], \
        [teamrooms_dict['snapshots']['snapshot']]), te.get_workdiaries(1, 1, 1)


teamrooms_dict_none = {'teamrooms': '',
                       'teamroom': '',
                       'snapshots': '',
                       'snapshot': ''
                       }


def patched_urlopen_teamrooms_none(*args, **kwargs):
    return MicroMock(data=json.dumps(teamrooms_dict_none), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_teamrooms_none)
def test_teamrooms_none():
    te = Team(get_client())

    #test full_url
    full_url = te.full_url('test')
    assert full_url == 'https://www.odesk.com/api/team/v1/test', full_url

    #test get_teamrooms
    assert te.get_teamrooms() == [], te.get_teamrooms()

    #test get_snapshots
    assert te.get_snapshots(1) == [], te.get_snapshots(1)

    #test get_snapshot
    assert te.get_snapshot(1, 1) == teamrooms_dict_none['snapshot'], te.get_snapshot(1, 1)


userroles = {u'userrole':
             [{u'parent_team__reference': u'1',
              u'user__id': u'testuser', u'team__id': u'test:t',
              u'reference': u'1', u'team__name': u'te',
              u'company__reference': u'1',
              u'user__reference': u'1',
              u'user__first_name': u'Test',
              u'user__last_name': u'Development',
              u'parent_team__id': u'testdev',
              u'team__reference': u'1', u'role': u'manager',
              u'affiliation_status': u'none', u'engagement__reference': u'',
              u'parent_team__name': u'TestDev', u'has_team_room_access': u'1',
              u'company__name': u'Test Dev',
              u'permissions':
                {u'permission': [u'manage_employment', u'manage_recruiting']}}]}

engagement = {u'status': u'active',
              u'buyer_team__reference': u'1', u'provider__reference': u'2',
              u'job__title': u'development', u'roles': {u'role': u'buyer'},
              u'reference': u'1', u'engagement_end_date': u'',
              u'fixed_price_upfront_payment': u'0',
              u'fixed_pay_amount_agreed': u'1.00',
              u'provider__id': u'test_provider',
              u'buyer_team__id': u'testteam:aa',
              u'engagement_job_type': u'fixed-price',
              u'job__reference': u'1', u'provider_team__reference': u'',
              u'engagement_title': u'Developer',
              u'fixed_charge_amount_agreed': u'0.01',
              u'created_time': u'0000', u'provider_team__id': u'',
              u'offer__reference': u'',
              u'engagement_start_date': u'000', u'description': u''}

engagements = {u'lister':
               {u'total_items': u'10', u'query': u'',
                u'paging': {u'count': u'10', u'offset': u'0'}, u'sort': u''},
               u'engagement': [engagement, engagement],
               }

offer = {u'provider__reference': u'1',
         u'signed_by_buyer_user': u'',
         u'reference': u'1', u'job__description': u'python',
         u'buyer_company__name': u'Python community',
         u'engagement_title': u'developer', u'created_time': u'000',
         u'buyer_company__reference': u'2', u'buyer_team__id': u'testteam:aa',
         u'interview_status': u'in_process', u'buyer_team__reference': u'1',
         u'signed_time_buyer': u'', u'has_buyer_signed': u'',
         u'signed_time_provider': u'', u'created_by': u'testuser',
         u'job__reference': u'2', u'engagement_start_date': u'00000',
         u'fixed_charge_amount_agreed': u'0.01', u'provider_team__id': u'',
         u'status': u'', u'signed_by_provider_user': u'',
         u'engagement_job_type': u'fixed-price', u'description': u'',
         u'provider_team__name': u'', u'fixed_pay_amount_agreed': u'0.01',
         u'candidacy_status': u'active', u'has_provider_signed': u'',
         u'message_from_provider': u'', u'my_role': u'buyer',
         u'key': u'~~0001', u'message_from_buyer': u'',
         u'buyer_team__name': u'Python community 2',
         u'engagement_end_date': u'', u'fixed_price_upfront_payment': u'0',
         u'created_type': u'buyer', u'provider_team__reference': u'',
         u'job__title': u'translation', u'expiration_date': u'',
         u'engagement__reference': u''}

offers = {u'lister':
          {u'total_items': u'10', u'query': u'', u'paging':
           {u'count': u'10', u'offset': u'0'}, u'sort': u''},
           u'offer': [offer, offer]}

job = {u'subcategory': u'Development', u'reference': u'1',
       u'buyer_company__name': u'Python community',
       u'job_type': u'fixed-price', u'created_time': u'000',
       u'created_by': u'test', u'duration': u'',
       u'last_candidacy_access_time': u'',
       u'category': u'Web',
       u'buyer_team__reference': u'169108', u'title': u'translation',
       u'buyer_company__reference': u'1', u'num_active_candidates': u'0',
       u'buyer_team__name': u'Python community 2', u'start_date': u'000',
       u'status': u'filled', u'num_new_candidates': u'0',
       u'description': u'test', u'end_date': u'000',
       u'public_url': u'http://www.odesk.com/jobs/~~0001',
       u'visibility': u'invite-only', u'buyer_team__id': u'testteam:aa',
       u'num_candidates': u'1', u'budget': u'1000', u'cancelled_date': u'',
       u'filled_date': u'0000'}

jobs = [job, job]

task = {u'reference': u'test', u'company_reference': u'1',
          u'team__reference': u'1', u'user__reference': u'1',
          u'code': u'1', u'description': u'test task',
          u'url': u'http://url.odesk.com/task', u'level': u'1'}

tasks = [task, task]

auth_user = {u'first_name': u'TestF', u'last_name': u'TestL',
             u'uid': u'testuser', u'timezone_offset': u'0',
             u'timezone': u'Europe/Athens', u'mail': u'test_user@odesk.com',
             u'messenger_id': u'', u'messenger_type': u'yahoo'}

user = {u'status': u'active', u'first_name': u'TestF',
        u'last_name': u'TestL', u'reference': u'0001',
        u'timezone_offset': u'10800',
        u'public_url': u'http://www.odesk.com/users/~~000',
        u'is_provider': u'1',
        u'timezone': u'GMT+02:00 Athens, Helsinki, Istanbul',
        u'id': u'testuser'}

team = {u'status': u'active', u'parent_team__reference': u'0',
         u'name': u'Test',
         u'reference': u'1',
         u'company__reference': u'1',
         u'id': u'test',
         u'parent_team__id': u'test_parent',
         u'company_name': u'Test', u'is_hidden': u'',
         u'parent_team__name': u'Test parent'}

company = {u'status': u'active',
             u'name': u'Test',
             u'reference': u'1',
             u'company_id': u'1',
             u'owner_user_id': u'1', }

candidacy_stats = {u'job_application_quota': u'20',
                   u'job_application_quota_remaining': u'20',
                   u'number_of_applications': u'2',
                   u'number_of_interviews': u'3',
                   u'number_of_invites': u'0',
                   u'number_of_offers': u'0'}

hr_dict = {u'auth_user': auth_user,
           u'server_time': u'0000',
           u'user': user,
           u'team': team,
           u'company': company,
            u'teams': [team, team],
            u'companies': [company, company],
            u'users': [user, user],
            u'tasks': task,
            u'userroles': userroles,
            u'engagements': engagements,
            u'engagement': engagement,
            u'offer': offer,
            u'offers': offers,
            u'job': job,
            u'jobs': jobs,
            u'candidacy_stats': candidacy_stats}


def patched_urlopen_hr(*args, **kwargs):
    return MicroMock(data=json.dumps(hr_dict), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_get_hrv2_user():
    hr = get_client().hr

    #test get_user
    assert hr.get_user(1) == hr_dict[u'user'], hr.get_user(1)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_get_hrv2_companies():
    hr = get_client().hr
    #test get_companies
    assert hr.get_companies() == hr_dict[u'companies'], hr.get_companies()

    #test get_company
    assert hr.get_company(1) == hr_dict[u'company'], hr.get_company(1)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_get_hrv2_company_teams():
    hr = get_client().hr
    #test get_company_teams
    assert hr.get_company_teams(1) == hr_dict['teams'], hr.get_company_teams(1)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_get_hrv2_company_users():
    hr = get_client().hr
    #test get_company_users
    assert hr.get_company_users(1) == hr_dict['users'], hr.get_company_users(1)
    assert hr.get_company_users(1, False) == hr_dict['users'], \
         hr.get_company_users(1, False)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_get_hrv2_company_tasks():
    hr = get_client().hr
    #test get_company_tasks
    try:
        assert hr.get_company_tasks(1) == hr_dict['tasks'], \
            hr.get_company_tasks(1)
    except APINotImplementedException, e:
        pass
    except Exception, e:
        print e
        assert 0, ("APINotImplementedException not raised", e)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_get_hrv2_teams():
    hr = get_client().hr
    #test get_teams
    assert hr.get_teams() == hr_dict[u'teams'], hr.get_teams()

    #test get_team
    assert hr.get_team(1) == hr_dict[u'team'], hr.get_team(1)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_get_hrv2_team_users():
    hr = get_client().hr
    #test get_team_users
    assert hr.get_team_users(1) == hr_dict[u'users'], hr.get_team_users(1)
    assert hr.get_team_users(1, False) == hr_dict[u'users'], \
         hr.get_team_users(1, False)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_get_hrv2_team_tasks():
    hr = get_client().hr
    #test get_team_tasks
    try:
        assert hr.get_team_tasks(1) == hr_dict['tasks'], hr.get_team_tasks(1)
    except APINotImplementedException, e:
        pass
    except:
        assert 0, "APINotImplementedException not raised"


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_get_hrv2_userroles():
    hr = get_client().hr
    #test get_user_role
    assert hr.get_user_role(user_reference=1) == hr_dict['userroles'], \
                                                 hr.get_user_role(user_reference=1)
    assert hr.get_user_role(team_reference=1) == hr_dict['userroles'], \
                                                 hr.get_user_role(team_reference=1)
    assert hr.get_user_role() == hr_dict['userroles'], hr.get_user_role()

    try:
        assert hr.get_tasks() == hr_dict['tasks'], hr.get_tasks()
    except APINotImplementedException, e:
        pass
    except:
        assert 0, "APINotImplementedException not raised"


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_get_hrv2_jobs():
    hr = get_client().hr
    #test get_jobs
    assert hr.get_jobs() == hr_dict[u'jobs'], hr.get_jobs()
    assert hr.get_job(1) == hr_dict[u'job'], hr.get_job(1)
    assert hr.update_job(1, {'status': 'filled'}) == hr_dict, hr.update_job(1, {'status': 'filled'})
    assert hr.delete_job(1, 41) == hr_dict, hr.delete_job(1, 41)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_get_hrv2_offers():
    hr = get_client().hr
    #test get_offers
    assert hr.get_offers() == hr_dict[u'offers'], hr.get_offers()
    assert hr.get_offer(1) == hr_dict[u'offer'], hr.get_offer(1)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_get_hrv2_engagements():
    hr = get_client().hr
    #test get_engagements
    assert hr.get_engagements() == hr_dict[u'engagements'], hr.get_engagements()
    assert hr.get_engagement(1) == hr_dict[u'engagement'], hr.get_engagement(1)


adjustments = {u'adjustment': {u'reference': '100'}}


def patched_urlopen_hradjustment(*args, **kwargs):
    return MicroMock(data=json.dumps(adjustments), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hradjustment)
def test_hrv2_post_adjustment():
    hr = get_client().hr

    result = hr.post_team_adjustment(1, 2, 100000, 'test', 'test note')
    assert result == adjustments[u'adjustment'], result


job_data = {
                'buyer_team_reference': 111,
                'title': 'Test job from API',
                'job_type': 'hourly',
                'description': 'this is test job, please do not apply to it',
                'visibility': 'odesk',
                'duration': 10,
                'category': 'Web Development',
                'subcategory': 'Other - Web Development',
                }


def patched_urlopen_job_data_parameters(self, method, url, **kwargs):
    post_dict = urlparse.parse_qs(kwargs.get('body'))
    assert post_dict == {'api_key': ['public'], 'job_data[subcategory]': ['Other - Web Development'], 'job_data[description]': ['this is test job, please do not apply to it'], 'job_data[duration]': ['10'], 'job_data[buyer_team_reference]': ['111'], 'job_data[job_type]': ['hourly'], 'api_token': ['some_token'], 'api_sig': ['830fb250d089dabb2e74a301796c6e6b'], 'job_data[title]': ['Test job from API'], 'job_data[visibility]': ['odesk'], 'job_data[category]': ['Web Development']}, a
    return MicroMock(data='{"some":"data"}', status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_job_data_parameters)
def test_job_data_parameters():
    hr = get_client().hr
    result = hr.post_job(job_data)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_get_hrv2_candidacy_stats():
    hr = get_client().hr
    #test get_candidacy_stats
    result = hr.get_candidacy_stats()
    assert result == hr_dict['candidacy_stats'], result


provider_dict = {'profile':
                 {u'response_time': u'31.0000000000000000',
                  u'dev_agency_ref': u'',
                  u'dev_adj_score_recent': u'0',
                  u'dev_ui_profile_access': u'Public',
                  u'dev_portrait': u'',
                  u'dev_ic': u'Freelance Provider',
                  u'certification': u'',
                  u'dev_usr_score': u'0',
                  u'dev_country': u'Ukraine',
                  u'dev_recent_rank_percentile': u'0',
                  u'dev_profile_title': u'Python developer',
                  u'dev_groups': u'',
                  u'dev_scores':
                  {u'dev_score':
                   [{u'description': u'competency and skills for the job, understanding of specifications/instructions',
                     u'avg_category_score_recent': u'',
                     u'avg_category_score': u'',
                     u'order': u'1', u'label': u'Skills'},
                     {u'description': u'quality of work deliverables',
                      u'avg_category_score_recent': u'',
                      u'avg_category_score': u'', u'order': u'2', u'label': u'Quality'},
                      ]
                   }},
                   'providers': {'test': 'test'},
                   'jobs': {'test': 'test'},
                   'otherexp': 'experiences',
                   'skills': 'skills',
                   'tests': 'tests',
                   'certificates': 'certificates',
                   'employments': 'employments',
                   'educations': 'employments',
                   'projects': 'projects',
                   'quick_info': 'quick_info',
                   'categories': 'category 1',
                   'regions': 'region 1',
                   'tests': 'test 1',
                   }


def patched_urlopen_provider(*args, **kwargs):
    return MicroMock(data=json.dumps(provider_dict), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_provider)
def test_provider():
    pr = get_client().provider

    #test full_url
    full_url = pr.full_url('test')
    assert full_url == 'https://www.odesk.com/api/profiles/v1/test', full_url

    #test get_provider
    assert pr.get_provider(1) == provider_dict['profile'], pr.get_provider(1)

    #test get_provider_brief
    assert pr.get_provider_brief(1) == provider_dict['profile'], \
        pr.get_provider_brief(1)

    #test search_providers
    assert pr.search_providers(data={'a': 1}) == provider_dict['providers'], \
        pr.search_providers(data={'a': 1})

    #test search_jobs
    assert pr.search_jobs(data={'a': 1}) == provider_dict['jobs'], \
        pr.get_jobs(data={'a': 1})

    assert pr.get_skills(1) == provider_dict['skills'], \
        pr.get_skills(1)

    assert pr.add_skill(1, {'skill': 'skill'}) == provider_dict, \
        pr.add_skill(1, {'skill': 'skill'})

    assert pr.update_skill(1, 1, {'skill': 'skill'}) == provider_dict, \
        pr.update_skill(1, 1, {'skill': 'skill'})

    assert pr.delete_skill(1, 1) == provider_dict, \
        pr.delete_skill(1, 1)

    assert pr.get_quickinfo(1) == provider_dict['quick_info'], \
        pr.get_quickinfo(1)

    assert pr.update_quickinfo(1, {'quickinfo': 'quickinfo'}) == provider_dict, \
        pr.update_quickinfo(1, {'quickinfo': 'quickinfo'})

    result = pr.get_affiliates(1)
    assert result == provider_dict['profile']

    result = pr.get_categories_metadata()
    assert result == provider_dict['categories']

    result = pr.get_skills_metadata()
    assert result == provider_dict['skills']

    result = pr.get_regions_metadata()
    assert result == provider_dict['regions']

    result = pr.get_tests_metadata()
    assert result == provider_dict['tests']


trays_dict = {'trays': [{u'unread': u'0',
              u'type': u'sent',
              u'id': u'1',
              u'tray_api': u'/api/mc/v1/trays/username/sent.json'},
              {u'unread': u'0',
               u'type': u'inbox',
               u'id': u'2',
               u'tray_api': u'/api/mc/v1/trays/username/inbox.json'},
              {u'unread': u'0',
               u'type': u'notifications',
               u'id': u'3',
               u'tray_api': u'/api/mc/v1/trays/username/notifications.json'}]}


def patched_urlopen_trays(*args, **kwargs):
    return MicroMock(data=json.dumps(trays_dict), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_trays)
def test_get_trays():
    mc = get_client().mc

    #test full_url
    full_url = mc.full_url('test')
    assert full_url == 'https://www.odesk.com/api/mc/v1/test', full_url

    #test get_trays
    assert mc.get_trays(1) == trays_dict['trays'], mc.get_trays(1)
    assert mc.get_trays(1, paging_offset=10, paging_count=10) ==\
         trays_dict['trays'], mc.get_trays(1, paging_offset=10, paging_count=10)


tray_content_dict = {"current_tray": {"threads": '1'}}


def patched_urlopen_tray_content(*args, **kwargs):
    return MicroMock(data=json.dumps(tray_content_dict), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_tray_content)
def test_get_tray_content():
    mc = get_client().mc

    #test get_tray_content
    assert mc.get_tray_content(1, 1) ==\
         tray_content_dict['current_tray']['threads'], mc.get_tray_content(1, 1)
    assert mc.get_tray_content(1, 1, paging_offset=10, paging_count=10) ==\
         tray_content_dict['current_tray']['threads'], \
         mc.get_tray_content(1, 1, paging_offset=10, paging_count=10)


thread_content_dict = {"thread": {"test": '1'}}


def patched_urlopen_thread_content(*args, **kwargs):
    return MicroMock(data=json.dumps(thread_content_dict), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_thread_content)
def test_get_thread_content():
    mc = get_client().mc

    #test get_provider
    assert mc.get_thread_content(1, 1) ==\
         thread_content_dict['thread'], mc.get_thread_content(1, 1)
    assert mc.get_thread_content(1, 1, paging_offset=10, paging_count=10) ==\
         thread_content_dict['thread'], \
         mc.get_thread_content(1, 1, paging_offset=10, paging_count=10)


read_thread_content_dict = {"thread": {"test": '1'}}


def patched_urlopen_read_thread_content(*args, **kwargs):
    return MicroMock(data=json.dumps(read_thread_content_dict), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_read_thread_content)
def test_put_threads_read_unread():
    mc = get_client().mc

    read = mc.put_threads_read('test', [1, 2, 3])
    assert read == read_thread_content_dict, read

    unread = mc.put_threads_read('test', [5, 6, 7])
    assert unread == read_thread_content_dict, unread

    read = mc.put_threads_unread('test', [1, 2, 3])
    assert read == read_thread_content_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_read_thread_content)
def test_put_threads_starred_unstarred():
    mc = get_client().mc

    starred = mc.put_threads_starred('test', [1, 2, 3])
    assert starred == read_thread_content_dict, starred

    unstarred = mc.put_threads_unstarred('test', [5, 6, 7])
    assert unstarred == read_thread_content_dict, unstarred


@patch('urllib3.PoolManager.urlopen', patched_urlopen_read_thread_content)
def test_put_threads_deleted_undeleted():
    mc = get_client().mc

    deleted = mc.put_threads_deleted('test', [1, 2, 3])
    assert deleted == read_thread_content_dict, deleted

    undeleted = mc.put_threads_undeleted('test', [5, 6, 7])
    assert undeleted == read_thread_content_dict, undeleted


@patch('urllib3.PoolManager.urlopen', patched_urlopen_read_thread_content)
def test_post_message():
    mc = get_client().mc

    message = mc.post_message('username', 'recepient1,recepient2', 'subject',
                              'body')
    assert message == read_thread_content_dict, message

    message = mc.post_message('username', ('recepient1@sss',\
        'recepient`іваівsss'), 'subject',
                              'body')
    assert message == read_thread_content_dict, message

    message = mc.post_message('username',\
        'recepient1@sss,1%&&|-!@#recepient`іваівsss', 'subject',
                              'body')
    assert message == read_thread_content_dict, message

    reply = mc.post_message('username', 'recepient1,recepient2', 'subject',
                              'body', 123)
    assert reply == read_thread_content_dict, reply


timereport_dict = {u'table':
     {u'rows':
      [{u'c':
        [{u'v': u'20100513'},
         {u'v': u'company1:team1'},
         {u'v': u'1'},
         {u'v': u'1'},
         {u'v': u'0'},
         {u'v': u'1'},
         {u'v': u'Bug 1: Test'}]}],
         u'cols':
         [{u'type': u'date', u'label': u'worked_on'},
          {u'type': u'string', u'label': u'assignment_team_id'},
          {u'type': u'number', u'label': u'hours'},
          {u'type': u'number', u'label': u'earnings'},
          {u'type': u'number', u'label': u'earnings_offline'},
          {u'type': u'string', u'label': u'task'},
          {u'type': u'string', u'label': u'memo'}]}}


def patched_urlopen_timereport_content(*args, **kwargs):
    return MicroMock(data=json.dumps(timereport_dict), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_timereport_content)
def test_get_provider_timereport():
    tc = get_client().timereport

    read = tc.get_provider_report('test',\
        utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == timereport_dict, read

    read = tc.get_provider_report('test',\
        utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)),
                                                hours=True)
    assert read == timereport_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_timereport_content)
def test_get_company_timereport():
    tc = get_client().timereport

    read = tc.get_company_report('test',\
        utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == timereport_dict, read

    read = tc.get_company_report('test',\
        utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)),
                                  hours=True)
    assert read == timereport_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_timereport_content)
def test_get_agency_timereport():
    tc = get_client().timereport

    read = tc.get_agency_report('test', 'test',\
        utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == timereport_dict, read

    read = tc.get_agency_report('test', 'test',\
        utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)),
                                  hours=True)
    assert read == timereport_dict, read

fin_report_dict = {u'table':
     {u'rows':
      [{u'c':
        [{u'v': u'20100513'},
         {u'v': u'odesk:odeskps'},
         {u'v': u'1'},
         {u'v': u'1'},
         {u'v': u'0'},
         {u'v': u'1'},
         {u'v': u'Bug 1: Test'}]}],
         u'cols':
         [{u'type': u'date', u'label': u'worked_on'},
          {u'type': u'string', u'label': u'assignment_team_id'},
          {u'type': u'number', u'label': u'hours'},
          {u'type': u'number', u'label': u'earnings'},
          {u'type': u'number', u'label': u'earnings_offline'},
          {u'type': u'string', u'label': u'task'},
          {u'type': u'string', u'label': u'memo'}]}}


def patched_urlopen_fin_report_content(*args, **kwargs):
    return MicroMock(data=json.dumps(fin_report_dict), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_fin_report_content)
def test_get_provider_billings():
    fr = get_client().finreport

    read = fr.get_provider_billings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_fin_report_content)
def test_get_provider_teams_billings():
    fr = get_client().finreport

    read = fr.get_provider_teams_billings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_fin_report_content)
def test_get_provider_companies_billings():
    fr = get_client().finreport

    read = fr.get_provider_companies_billings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_fin_report_content)
def test_get_provider_earnings():
    fr = get_client().finreport

    read = fr.get_provider_earnings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_fin_report_content)
def test_get_provider_teams_earnings():
    fr = get_client().finreport

    read = fr.get_provider_teams_earnings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_fin_report_content)
def test_get_provider_companies_earnings():
    fr = get_client().finreport

    read = fr.get_provider_companies_earnings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_fin_report_content)
def test_get_buyer_teams_billings():
    fr = get_client().finreport

    read = fr.get_buyer_teams_billings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_fin_report_content)
def test_get_buyer_companies_billings():
    fr = get_client().finreport

    read = fr.get_buyer_companies_billings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_fin_report_content)
def test_get_buyer_teams_earnings():
    fr = get_client().finreport

    read = fr.get_buyer_teams_earnings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_fin_report_content)
def test_get_buyer_companies_earnings():
    fr = get_client().finreport

    read = fr.get_buyer_companies_earnings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_fin_report_content)
def test_get_financial_entities():
    fr = get_client().finreport

    read = fr.get_financial_entities('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_fin_report_content)
def test_get_financial_entities_provider():
    fr = get_client().finreport

    read = fr.get_financial_entities_provider('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


def test_get_version():
    import odesk
    odesk.VERSION = (1, 2, 3, 'alpha', 2)

    assert get_version() == '1.2.3 alpha 2', get_version()

    odesk.VERSION = (1, 2, 3, 'alpha', 0)
    assert get_version() == '1.2.3 pre-alpha', get_version()


task_dict = {u'tasks': 'task1'}


def patched_urlopen_task(*args, **kwargs):
    return MicroMock(data=json.dumps(task_dict), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_get_company_tasks():
    task = get_client().task

    assert task.get_company_tasks(1) == task_dict['tasks'], \
     task.get_company_tasks(1)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_get_team_tasks():
    task = get_client().task

    assert task.get_team_tasks(1, 1) == task_dict['tasks'], \
     task.get_team_tasks(1, 1)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_get_user_tasks():
    task = get_client().task

    assert task.get_user_tasks(1, 1, 1) == task_dict['tasks'], \
     task.get_user_tasks(1, 1, 1)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_company_tasks_full():
    task = get_client().task

    assert task.get_company_tasks_full(1) == task_dict['tasks'], \
     task.get_company_tasks_full(1)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_get_team_tasks_full():
    task = get_client().task

    assert task.get_team_tasks_full(1, 1) == task_dict['tasks'], \
     task.get_team_tasks_full(1, 1)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_get_user_tasks_full():
    task = get_client().task

    assert task.get_user_tasks_full(1, 1, 1) == task_dict['tasks'], \
     task.get_user_tasks_full(1, 1, 1)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_get_company_specific_tasks():
    task = get_client().task

    assert task.get_company_specific_tasks(1, [1, 1]) == task_dict['tasks'], \
     task.get_company_specific_tasks(1, [1, 1])


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_get_team_specific_tasks():
    task = get_client().task

    assert task.get_team_specific_tasks(1, 1, [1, 1]) == task_dict['tasks'], \
     task.get_team_specific_tasks(1, 1, [1, 1])


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_get_user_specific_tasks():
    task = get_client().task

    assert task.get_user_specific_tasks(1, 1, 1, [1, 1]) == task_dict['tasks'], \
     task.get_user_specific_tasks(1, 1, 1, [1, 1])


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_post_company_task():
    task = get_client().task

    assert task.post_company_task(1, 1, '1', 'ttt') == task_dict, \
     task.post_company_task(1, 1, '1', 'ttt')


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_post_team_task():
    task = get_client().task

    assert task.post_team_task(1, 1, 1, '1', 'ttt') == task_dict, \
     task.post_team_task(1, 1, 1, '1', 'ttt')


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_post_user_task():
    task = get_client().task

    assert task.post_user_task(1, 1, 1, 1, '1', 'ttt') == task_dict, \
     task.post_user_task(1, 1, 1, 1, '1', 'ttt')


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_put_company_task():
    task = get_client().task

    assert task.put_company_task(1, 1, '1', 'ttt') == task_dict, \
     task.put_company_task(1, 1, '1', 'ttt')


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_put_team_task():
    task = get_client().task

    assert task.put_team_task(1, 1, 1, '1', 'ttt') == task_dict, \
     task.put_team_task(1, 1, 1, '1', 'ttt')


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_put_user_task():
    task = get_client().task

    assert task.put_user_task(1, 1, 1, 1, '1', 'ttt') == task_dict, \
     task.put_user_task(1, 1, 1, 1, '1', 'ttt')


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_delete_company_task():
    task = get_client().task

    assert task.delete_company_task(1, [1, 1]) == task_dict, \
     task.delete_company_task(1, [1, 1])


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_delete_team_task():
    task = get_client().task

    assert task.delete_team_task(1, 1, [1, 1]) == task_dict, \
     task.delete_team_task(1, 1, [1, 1])


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_delete_user_task():
    task = get_client().task

    assert task.delete_user_task(1, 1, 1, [1, 1]) == task_dict, \
     task.delete_user_task(1, 1, 1, [1, 1])


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_delete_all_company_tasks():
    task = get_client().task

    assert task.delete_all_company_tasks(1) == task_dict, \
     task.delete_all_company_tasks(1)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_delete_all_team_tasks():
    task = get_client().task

    assert task.delete_all_team_tasks(1, 1) == task_dict, \
     task.delete_all_team_tasks(1, 1)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_delete_all_user_tasks():
    task = get_client().task

    assert task.delete_all_user_tasks(1, 1, 1) == task_dict, \
     task.delete_all_user_tasks(1, 1, 1)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_update_batch_tasks():
    task = get_client().task

    assert task.update_batch_tasks(1, "1;2;3") == task_dict, \
     task.update_batch_tasks(1, "1;2;3")


def test_gds_namespace():
    from odesk.namespaces import GdsNamespace
    gds = GdsNamespace(get_client())

    assert gds.post('test.url', {}) is None, \
        gds.post('test.url', {})
    assert gds.put('test.url', {}) is None, \
        gds.put('test.url', {})
    assert gds.delete('test.url', {}) is None, \
        gds.delete('test.url', {})


@patch('urllib3.PoolManager.urlopen', patched_urlopen)
def test_gds_namespace_get():
    from odesk.namespaces import GdsNamespace
    gds = GdsNamespace(get_client())
    result = gds.get('http://test.url')
    assert isinstance(result, dict), type(res)
    assert result == sample_json_dict, (result, sample_json_dict)


def get_oauth_client():
    key = '56adf4b66aaf61444a77796c17c0da53'
    secret = 'e5864a0bcbed2085'
    return Client(key, secret, auth='oauth')

def setup_oauth():
    return OAuth(get_oauth_client())

def test_oauth_full_url():
    oa = setup_oauth()
    request_token_url = oa.full_url('oauth/token/request')
    access_token_url = oa.full_url('oauth/token/access')
    assert request_token_url == oa.request_token_url, request_token_url
    assert access_token_url == oa.access_token_url, access_token_url

def patched_httplib2_request(*args, **kwargs):
    return {'status': '200'},\
        'oauth_callback_confirmed=1&oauth_token=709d434e6b37a25c50e95b0e57d24c46&oauth_token_secret=193ef27f57ab4e37'

@patch('httplib2.Http.request', patched_httplib2_request)
def test_oauth_get_request_token():
    oa = setup_oauth()
    assert oa.get_request_token() == ('709d434e6b37a25c50e95b0e57d24c46',\
                                    '193ef27f57ab4e37')

@patch('httplib2.Http.request', patched_httplib2_request)
def test_oauth_get_authorize_url():
    oa = setup_oauth()
    assert oa.get_authorize_url() ==\
        'https://www.odesk.com/services/api/auth?oauth_token=709d434e6b37a25c50e95b0e57d24c46'
    assert oa.get_authorize_url('http://example.com/oauth/complete') ==\
        'https://www.odesk.com/services/api/auth?oauth_token=709d434e6b37a25c50e95b0e57d24c46&oauth_callback=http%3A%2F%2Fexample.com%2Foauth%2Fcomplete'

def patched_httplib2_access(*args, **kwargs):
    return {'status': '200'},\
        'oauth_token=aedec833d41732a584d1a5b4959f9cd6&oauth_token_secret=9d9cccb363d2b13e'

@patch('httplib2.Http.request', patched_httplib2_access)
def test_oauth_get_access_token():
    oa = setup_oauth()
    oa.request_token = '709d434e6b37a25c50e95b0e57d24c46'
    oa.request_token_secret = '193ef27f57ab4e37'
    assert oa.get_access_token('9cbcbc19f8acc2d85a013e377ddd4118') ==\
     ('aedec833d41732a584d1a5b4959f9cd6', '9d9cccb363d2b13e')


job_profiles_dict = {'profiles': {'profile': [
    {
        u'amount': u'',
        u'as_hrs_per_week': u'0',
        u'as_job_type': u'Hourly',
        u'as_opening_access': u'private',
        u'as_opening_recno': u'111',
        u'as_opening_title': u'Review website and improve copy writing',
        u'as_provider': u'111',
        u'as_rate': u'$10.00',
        u'as_reason': u'Job was cancelled or postponed',
        u'as_reason_api_ref': u'',
        u'as_reason_recno': u'72',
        u'as_recno': u'1',
        u'as_status': u'Closed',
        u'as_to': u'11/2011',
        u'as_total_charge': u'84',
        u'as_total_hours': u'3.00',
        u'op_desc_digest': u'Test job 1.',
        u'op_description': u'Test job 1.',
        u'ciphertext': u'~~111111111',
        u'ui_job_profile_access': u'odesk',
        u'ui_opening_status': u'Active',
        u'version': u'1'
    },
    {
        u'amount': u'',
        u'as_hrs_per_week': u'0',
        u'as_job_type': u'Hourly',
        u'as_opening_access': u'private',
        u'as_opening_recno': u'222',
        u'as_opening_title': u'Review website and improve copy writing',
        u'as_provider': u'222',
        u'as_rate': u'$10.00',
        u'as_reason': u'Job was cancelled or postponed',
        u'as_reason_api_ref': u'',
        u'as_reason_recno': u'72',
        u'as_recno': u'2',
        u'as_status': u'Closed',
        u'as_to': u'11/2011',
        u'as_total_charge': u'84',
        u'as_total_hours': u'3.00',
        u'ciphertext': u'~~222222222',
        u'op_desc_digest': u'Test job 2.',
        u'op_description': u'Test job 2.',
        u'ui_job_profile_access': u'odesk',
        u'ui_opening_status': u'Active',
        u'version': u'1'
    },
]}}

job_profile_dict = {'profile':
    {
        u'amount': u'',
        u'as_hrs_per_week': u'0',
        u'as_job_type': u'Hourly',
        u'as_opening_access': u'private',
        u'as_opening_recno': u'111',
        u'as_opening_title': u'Review website and improve copy writing',
        u'as_provider': u'111',
        u'as_rate': u'$10.00',
        u'as_reason': u'Job was cancelled or postponed',
        u'as_reason_api_ref': u'',
        u'as_reason_recno': u'72',
        u'as_recno': u'1',
        u'as_status': u'Closed',
        u'as_to': u'11/2011',
        u'as_total_charge': u'84',
        u'as_total_hours': u'3.00',
        u'op_desc_digest': u'Test job 1.',
        u'op_description': u'Test job 1.',
        u'ciphertext': u'~~111111111',
        u'ui_job_profile_access': u'odesk',
        u'ui_opening_status': u'Active',
        u'version': u'1'
    }
}


def patched_urlopen_single_job(*args, **kwargs):
    return MicroMock(data=json.dumps(job_profile_dict), status=200)


def patched_urlopen_multiple_jobs(*args, **kwargs):
    return MicroMock(data=json.dumps(job_profiles_dict), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_single_job)
def test_single_job_profile():
    job = get_client().job

    # Test full_url
    full_url = job.full_url('jobs/111')
    assert full_url == 'https://www.odesk.com/api/profiles/v1/jobs/111', \
        full_url

    # Test input parameters
    try:
        job.get_job_profile({})
        raise Exception('Request should raise ValueError exception.')
    except ValueError, e:
        assert 'Invalid job key' in str(e)
    try:
        job.get_job_profile(['~~{0}'.format(x) for x in range(21)])
        raise Exception('Request should raise ValueError exception.')
    except ValueError, e:
        assert 'Number of keys per request is limited' in str(e)
    try:
        job.get_job_profile(['~~111111', 123456])
        raise Exception('Request should raise ValueError exception.')
    except ValueError, e:
        assert 'List should contain only job keys not recno' in str(e)

    # Get single job profile test
    assert job.get_job_profile('~~111111111') == job_profile_dict['profile'], \
        job.get_job_profile('~~111111111')


@patch('urllib3.PoolManager.urlopen', patched_urlopen_multiple_jobs)
def test_multiple_job_profiles():
    job = get_client().job

    # Test full_url
    full_url = job.full_url('jobs/~~111;~~222')
    assert full_url == \
        'https://www.odesk.com/api/profiles/v1/jobs/~~111;~~222', full_url

    # Get multiple job profiles test
    assert job.get_job_profile(['~~111111111', '~~222222222']) == \
        job_profiles_dict['profiles']['profile'], \
        job.get_job_profile(['~~111111111', '~~222222222'])
