import data_collection as dc
import properties.models as mods

session, response, page_count, sitemap = dc.initialize_session()

group = mods.SourceSiteGroup.objects.get(pk=sitemap['group'])
site = mods.SourceSite.objects.get(pk=sitemap['sites'][5])

if len(site.branches.filter(url='https://ocfintax.ongov.net/Imate/propdetail.aspx', origin=group)) == 0:
    general_info_site = site.branches.create(url='https://ocfintax.ongov.net/Imate/propdetail.aspx', origin=group)
else:
    general_info_site = site.branches.get(url='https://ocfintax.ongov.net/Imate/propdetail.aspx', origin=group)

dc.retrieve_tax_info(session, group, general_info_site)