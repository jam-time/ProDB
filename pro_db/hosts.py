import django
from django.db import models
import properties.models as mods
import requests
import re


class Host:
    def __init__(self):
        self.name = str
        self.url = str
        self.record = models.Model
        self.session = requests.Session
        self.last_response = requests.Response
        self.table_page_count = int
        self.table_page_count_pattern = str
        self.table_page = int
        self.table_url = str

    def initialize_record(self):
        if self.name == '' and self.url == '':
            return ('name and url are empty')

        if mods.SourceSiteGroup.objects.filter(name=self.name, origin_url=self.url).count() == 0:
            self.record = mods.SourceSiteGroup.get(name=self.name, origin_url=self.url)
        else:
            self.record = mods.SourceSiteGroup.create(name=self.name, origin_url=self.url)


class Onondaga(Host):
    def __init__(self):
        super().__init__()
        self.precursor_site_data = [
            {
                'url': 'https://ocfintax.ongov.net/Imate/index.aspx',
                'data': None,
                'params': None,
                'request_type': 'get',
            },
            {
                'url': 'https://ocfintax.ongov.net/Imate/index.aspx',
                'data': {'__EVENTTARGET': 'btnPublicAccess'},
                'params': None,
                'request_type': 'post'
            },
            {
                'url': 'https://ocfintax.ongov.net/Imate/disclaimer.aspx',
                'data': {'__EVENTTARGET': 'btnSubmit', 'btnSubmit': 'Continue', 'chkAgree': 'on'},
                'params': None,
                'request_type': 'post',
            },
            {
                'url': 'https://ocfintax.ongov.net/Imate/search.aspx',
                'data': None,
                'params': None,
                'request_type': 'get',
            },
            {
                'url': 'https://ocfintax.ongov.net/Imate/search.aspx',
                'data': None,
                'params': {'advanced': 'true'},
                'request_type': 'get',
            },
            {
                'url': 'https://ocfintax.ongov.net/Imate/search.aspx',
                'data': {
                    "ddlMunic": "all",
                    "txtPropNum": "",
                    "txtTaxMapNum": "",
                    "txtStreetNum": "",
                    "txtStreetName": "",
                    "ddlSiteType": "res",
                    "ddlStatus": "any",
                    "btnSearch": "Search",
                    "hiddenInputToUpdateATBuffer_CommonToolkitScripts": "1"
                },
                'params': {'advanced': 'true'},
                'request_type': 'post'
            }
        ]

    def initialize_session(self):
        self.name = 'Onondaga'
        self.url = 'https://ocfintax.ongov.net/Imate/index.aspx'
        self.table_url = 'https://ocfintax.ongov.net/Imate/viewlist.aspx'
        self.table_page_count_pattern = r'[\w\W]*?lblPageCount.>(\S*)<'
        self.initialize_record()
        self.session = requests.Session()

        view_state = r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(?P<view_state>.*)" />'
        view_state_generator = r'<input type="hidden" name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="(?P<view_state_generator>.*)" />'
        event_validation = r'<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(?P<event_validation>.*)" />'
        wildcard = r'[\w\W]'
        r_session_data = None

        for site in self.precursor_site_data:
            if r_session_data is not None:
                site['data']['__VIEWSTATE'] = m_session_data.group('view_state')
                site['data']['__VIEWSTATEGENERATOR'] = m_session_data.group('view_state_generator')
                site['data']['__EVENTVALIDATION'] = m_session_data.group('event_validation')

            self.last_response = self.session.request(site['request_type'].upper, site['url'], site['params'], site['data'])
            r_session_data = re.compile(f'{wildcard}*{view_state}{wildcard}*{view_state_generator}{wildcard}*{event_validation}')
            m_session_data = r_session_data.match(self.last_response.text)

        if self.last_response.url == self.table_url:
            r_page_count = re.compile(self.table_page_count_pattern)
            m_page_count = r_page_count.findall(self.last_response.text)
            self.table_page_count = m_page_count.group('page_count')