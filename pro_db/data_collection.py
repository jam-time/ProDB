import django
import os
import re
import requests
import static

import properties.models as mods

os.environ['DJANGO_SETTINGS_MODULE'] = 'pro_db.settings'
django.setup()


def navigate_init_tree(session, site_group, site_tree, response=None, parent_record=None, parent_site=None):
    site_record = parent_record
    end_site = parent_site

    for site in site_tree:
        if end_site['context'] != 'initialization':
            return session, response, site_record, end_site

        end_site = site

        if site_group.sites.filter(url=site['url'], source=parent_record).count() == 1:
            site_record = site_group.sites.get(url=site['url'], source=parent_record)
        else:
            site_record = site_group.sites.create(url=site['url'], source=parent_record)

        if response is not None:
            end_site['data'] = site_group.generate_request_data(response.text, end_site['data'])

        if site['request_type'] == 'get':
            response = session.get(site['url'], data=end_site['data'], params=site['params'])
        elif site['request_type'] == 'post':
            response = session.post(site['url'], data=end_site['data'], params=site['params'])

        site_group.update_session(session)

        if site['context'] != 'initialization':
            return session, response, site_record, end_site
        elif site['sites'] is not None:
            session, response, site_record, end_site = navigate_init_tree(session, site_group, site['sites'], response, site_record, end_site)

    return session, response, site_record, end_site


def initialize_session(county):
    entity = static.ENTITIES[county]

    if mods.SourceSiteGroup.objects.filter(name=county).count() == 0:
        site_group = mods.SourceSiteGroup(name=county, origin_url=entity['url'], data_patterns=entity['data_patterns'])
        site_group.save()
    else:
        site_group = mods.SourceSiteGroup.objects.get(name=county, origin_url=entity['url'], data_patterns=entity['data_patterns'])

    session = requests.Session()
    session, response, site_record, site = navigate_init_tree(session, site_group, entity['sites'])

    if site['page_count_pattern'] is not None:
        page_count_pattern = re.compile(site['page_count_pattern'])
        m = page_count_pattern.match(response.text)
        page_count = m.group(1)
    else:
        page_count = None

    return session, response, site_group, site_record, page_count


def parse_table_data(site_group, text_to_parse, row_delimiter_pattern=r'<tr>[\w\W]*?</tr>', row_items_pattern=r'[\s\S]*=(?P<id>\S*)\'>(?P<owner>.*)</td>.*>(?P<street_num>.*)</td>.*>(?P<street>.*)</td>'):
    """
    :param site_group: properties.models.SourceSiteGroup() object for corresponding entity (county)
    :param text_to_parse: raw html text from property table
    :param row_delimiter_pattern: regex pattern to match an entire table row
    :param row_items_pattern: regex pattern to match all columns in row; items should be named
        - valid names: 'owner', 'street', 'street_num', 'tax_id', 'local_id', 'postal_code', 'city'
    """
    row_delimiter = re.compile(row_delimiter_pattern)
    table_rows = row_delimiter.findall(text_to_parse)
    row_item_delimiter = re.compile(row_items_pattern)

    for row in table_rows:
        print(' parsing site...', '')
        row_items = row_item_delimiter.match(row)

        if row_items is not None:
            if len(mods.Owner.objects.filter(name=row_items.group(3))) > 0:
                print(' getting owner...', '')
                owner = mods.Owner.objects.get(name=row_items.group(3))
            else:
                print(' creating owner...', '')
                owner = mods.Owner(name=row_items.group(3))

            owner.save()

            if len(mods.ExternalID.objects.filter(id_external=row_items.group(1), source=site_group, property=property)) > 0:
                print(' getting SWIS ID...', '')
                swis_id = mods.ExternalID.objects.get(id_external=row_items.group(1), source=site_group, property=property)
            else:
                print(' creating SWIS ID...', '')
                swis_id = site_group.external_ids.create(id_external=row_items.group(1), property=property)

            swis_id.save()

            if len(mods.ExternalID.objects.filter(id_external=row_items.group(2), source=site_group, property=property)) > 0:
                print(' getting tax ID...', '')
                tax_id = mods.ExternalID.objects.get(id_external=row_items.group(2), source=site_group, property=property)
            else:
                print(' creating tax ID...', '')
                tax_id = site_group.external_ids.create(id_external=row_items.group(2), property=property)

            tax_id.save()

            if len(mods.Property.objects.filter(owner=owner, street_num=row_items.group(4), street=row_items.group(5))) > 0:
                print(' getting property...', '')
                property = owner.properties.get(street_num=row_items.group(4), street=row_items.group(5))
                property.source_site_groups.add(site_group)
            else:
                print(' creating property...', '')
                property = owner.properties.create(street_num=row_items.group(4), street=row_items.group(5))
                property.source_site_groups.add(site_group)

            property.save()


def create_property_records():
    session, response, page_count, sitemap = initialize_session()
    site = sitemap['sites'][5]
    group = sitemap['group']
    scrape_and_save(group, response.text)

    for p in range(2, int(page_count)+1):
        print('Page ' + str(p) + '...', '')
        response = session.get(site.url, params={'page': p})
        group.update_session(session)
        scrape_and_save(group, response.text)
        print(' done.')


def get_general_property_details(session, site_group, source):
    url = 'https://ocfintax.ongov.net/Imate/propdetail.aspx'
    county = site_group.name
    entity = static.ENTITIES[county]

    if len(source.branches.filter(url=url)) == 0:
        details_site = source.branches.create(origin=site_group, url=url, data_patterns=entity['data_patterns'])
    else:
        details_site = source.branches.get(origin=site_group, url=url, data_patterns=entity['data_patterns'])

    for property in site_group.properties.all():
        swis_id = property.external_ids.get(type='SWIS')
        tax_id = property.external_ids.get(type='tax')
        param_dict = {'swis': swis_id.id_external, 'printkey': tax_id.id_external}

        response = session.get(url=details_site.url, params=param_dict)
        site_group.update_headers(session)


def retrieve_detailed_property_data(session, site_group):
    pass


def retrieve_tax_info(session, site_group, source):
    pattern = r'[\w\W]*etaxTemplateForm:payments_:0:amountDue2.*\$(.*)</span></td>'
    url = 'https://onondaga.go2gov.net/faces/accounts'
    county = site_group.name
    entity = static.ENTITIES[county]

    if len(source.branches.filter(url=url)) == 0:
        tax_site = source.branches.create(origin=site_group, url=url, data_patterns=entity['data_patterns'])
    else:
        tax_site = source.branches.get(origin=site_group, url=url, data_patterns=entity['data_patterns'])

    count = 0
    for property in site_group.properties.all():
        count += 1
        print(str(count) + '...', '')
        if len(property.tax_info.filter()) == 0:
            swis_id = property.external_ids.filter(type='SWIS')[0]
            tax_id = property.external_ids.filter(type='tax')[0]
            param_dict = {'number': str(swis_id.id_external) + str(tax_id.id_external), 'src': 'SDG'}

            response = session.get(url=tax_site.url, params=param_dict)
            site_group.update_session(session)

            m = re.match(pattern, response.text)

            try:
                tax_due = m.group(1).replace(',', '')

                if len(property.tax_info.filter()) >= 1:
                    tax_obj = property.tax_info.filter()[0]
                else:
                    tax_obj = property.tax_info.create()

                tax_obj.total_due = tax_due
                tax_obj.raw_text = response.text
                tax_obj.save()
                print('done.')
            except AttributeError:
                if len(property.tax_info.filter()) >= 1:
                    tax_obj = property.tax_info.filter()[0]
                else:
                    tax_obj = property.tax_info.create()

                tax_obj.total_due = 0
                tax_obj.raw_text = response.text
                tax_obj.save()
                print('no tax info.')

        else:
            print('done.')