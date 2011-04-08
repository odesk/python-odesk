"""
Python bindings to odesk API
python-odesk version 0.4
(C) 2010-2011 oDesk
"""

import cookielib
from datetime import date
import hashlib
import logging
import urllib
import urllib2


try:
    import json
except ImportError:
    import simplejson as json

from odesk.exceptions import *
from odesk.namespace import *
from odesk.utils import *


class OConomy(GdsNamespace):
    api_url = 'oconomy/'
    version = 1

    
    def get_summary(self, year=None, month=None):
        if month and year:
            url = 'home/summary/%s%s' % (str(year), str(month))
        else:
            url = 'home/summary'
        result = self.get(url)

        return result['home']['summary']

    def get_hours_worked_by_locations(self):
        url = 'home/hours_worked_by_locations'
        result = self.get(url)
        return result['home']['hours_worked_by_locations']


    def get_hours_worked_by_weeks(self):
        url = 'home/hours_worked_by_weeks'
        result = self.get(url)
        return result['home']['hours_worked_by_weeks']


    def get_top_countries_by_hours(self):
        url = 'home/top_countries_by_hours'
        result = self.get(url)
        return result['home']['top_countries_by_hours']


    def get_charges_by_categories(self):
        url = 'home/charges_by_categories'
        result = self.get(url)
        return result['home']['charges_by_categories']


    def get_most_requested_skills(self):
        url = 'home/most_requested_skills'
        result = self.get(url)
        return result['home']['most_requested_skills']


    def get_summary(self, year=None, month=None):
        if month and year:
            url = 'summary/%s%s' % (str(year), str(month))
        else:
            url = 'summary'
        result = self.get(url)

        return result


class NonauthGdsNamespace(GdsNamespace):
    '''
    This class does not add authentication parameters
    to request urls (api_sig, api_key & api_token)
    Some APIs return error if called with authentication parameters
    '''
    def urlopen(self, url, data={}, method='GET'):
        if method == 'GET':
            request = HttpRequest(url=url, data=data.copy(),
                    method=method)
            return urllib2.urlopen(request)
        return None


class NonauthOConomy(NonauthGdsNamespace):
    '''
    oConomy Reports API
    '''
    api_url = 'oconomy/'
    version = 1

    def get_monthly_summary(self, month):
        '''get_monthly_summary(month)

        Monthly oDesk job market report

        Paramters
          month     'YYYYMM' or a datetime.date object
        '''
        if isinstance(month, date):
            month = '%04d%02d' % (date.year, date.month)
        else:
            month = str(month)
            _month_fmt = 'YYYYMM'
            if not len(month) == len(_month_fmt):
                raise ValueError('Format of month parameter (%s) should be %s' % (month, _month_fmt))
        url = 'summary/%s' % month
        result = self.get(url)
        return result

    def get_hours_worked_by_locations(self):
        '''get_hours_worked_by_locations

        Hours worked by location report
        '''
        url = 'hours_worked_by_locations'
        result = self.get(url)
        return result

    def get_hours_worked_by_weeks(self):
        '''get_hours_worked_by_weeks()

        oConomy weekly growth report
        '''
        url = 'hours_worked_by_weeks'
        result = self.get(url)
        return result

    def get_top_countries_by_hours(self):
        '''get_top_countries_by_hours()

        Top countries by hours worked for last 30 days report
        '''
        url = 'top_countries_by_hours'
        result = self.get(url)
        return result

    def get_earnings_by_categories(self):
        '''get_earnings_by_categories()

        Earnings by category report
        '''
        url = 'charges_by_categories'
        result = self.get(url)
        return result

    def get_most_requested_skills(self):
        '''get_most_requested_skills()

        Monthly most requested skills report
        '''
        url = 'most_requested_skills'
        result = self.get(url)
        return result

