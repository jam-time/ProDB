"""


"""

HOSTS = [
    'onondaga'
]


ENTITIES = {
    'onondaga': {
        'data_patterns': [
            {
                'name': r'__VIEWSTATE',
                'start': r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="',
                'end': r'" />'
            },
            {
                'name': r'__VIEWSTATEGENERATOR',
                'start': r'<input type="hidden" name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="',
                'end': r'" />'
            },
            {
                'name': r'__EVENTVALIDATION',
                'start': r'<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="',
                'end': r'" />'
            }
        ],
        'property_table_patterns': {
            'table_row_delimiter': r'<tr>[\w\W]*?</tr>',
            'row_item_delimiter': r'[\w\W]*swis=(?P<local_id>\S{6}).*printkey=(?P<tax_id>\S*)\'.*>(?P<owner>.*)</td>.*>(?P<street_num>.*)</td>.*>(?P<street>.*)</td>'
        },
        'sites': [
            {
                'url': 'https://ocfintax.ongov.net/Imate/index.aspx',
                'context': 'initialization',
                'data': None,
                'params': None,
                'request_type': 'get',
                'sites': None
            },
            {
                'url': 'https://ocfintax.ongov.net/Imate/index.aspx',
                'context': 'initialization',
                'data': {'__EVENTTARGET': 'btnPublicAccess'},
                'params': None,
                'request_type': 'post',
                'sites': [
                    {
                        'url': 'https://ocfintax.ongov.net/Imate/disclaimer.aspx',
                        'context': 'initialization',
                        'data': {'__EVENTTARGET': 'btnSubmit', 'btnSubmit': 'Continue', 'chkAgree': 'on'},
                        'params': None,
                        'request_type': 'post',
                        'sites': [
                            {
                                'url': 'https://ocfintax.ongov.net/Imate/search.aspx',
                                'context': 'initialization',
                                'data': None,
                                'params': None,
                                'request_type': 'get',
                                'sites': None
                            },
                            {
                                'url': 'https://ocfintax.ongov.net/Imate/search.aspx',
                                'context': 'initialization',
                                'data': None,
                                'params': {'advanced': 'true'},
                                'request_type': 'get',
                                'sites': None
                            },
                            {
                                'url': 'https://ocfintax.ongov.net/Imate/search.aspx',
                                'context': 'initialization',
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
                                'request_type': 'post',
                                'sites': [
                                    {
                                        'url': 'https://ocfintax.ongov.net/Imate/viewlist.aspx',
                                        'context': 'collection',
                                        'page_count_pattern': r'[\w\W]*?lblPageCount.>(\S*)<',
                                        'data': None,
                                        'params': {'sort': 'printkey', 'swis': 'all', 'sitetype': 'res', 'advanced': 'true'},
                                        'request_type': 'get',
                                        'sites': None
                                    },
                                    {
                                        'url': 'https://onondaga.go2gov.net/faces/accounts',
                                        'context': 'collection',
                                        'page_count_pattern': None,
                                        'data': None,
                                        'params': {'number': str, 'src': 'SDG'},
                                        'request_type': 'get',
                                        'sites': None
                                    },
                                    {
                                        'url': 'https://onondaga.go2gov.net/faces/accounts',
                                        'context': 'collection',
                                        'page_count_pattern': None,
                                        'data': None,
                                        'params': {'number': str, 'src': 'SDG'},
                                        'request_type': 'get',
                                        'sites': None
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
}
