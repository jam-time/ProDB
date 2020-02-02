import properties.models as mods
from django.db.models import Q


class Custodian:
    def __init__(self, group=None):
        self.group = group

    def sanitize_properties(self):
        if self.group is not None:
            all_properties = mods.Property.objects.filter(source_site_groups=self.group)
        else:
            all_properties = mods.Property.objects.filter()

        delete_list = []
        count = 0

        for property in all_properties:
            count += 1
            print(str(count) + '...', ' ')
            ext_id = property.external_ids.filter()[0]
            ext_id_q = Q(external_ids__id_external=ext_id.id_external)
            street_q = Q(street=property.street)
            street_num_q = Q(street_num=property.street_num)
            prop_id_q = ~Q(id=property.id)
            dupes = mods.Property.objects.filter(ext_id_q & street_q & street_num_q & prop_id_q)

            if dupes.count() > 0:
                print(str(dupes.count()) + ' duplicates...', ' ')
                for d in dupes:
                    owners = d.owners.all()
                    site_groups = d.source_site_groups.all()

                    for o in owners:
                        property.owners.add(o)

                    for sg in site_groups:
                        property.site_groups.add(sg)

                    for eid in d.external_ids.all():
                        if property.external_ids.filter(id_external=eid.id_external).count() > 0:
                            eid.delete()
                        else:
                            eid.property = property
                            eid.save()

                    for tax_info in d.tax_info.all():
                        if tax_info.total_gross_taxes() == property.tax_info.total_gross_taxes() and tax_info.year_summaries.filter().count() == property.tax_info.year_summaries.filter().count():
                            tax_info.delete()
                        else:
                            tax_info.property = property
                            tax_info.save()

                    for assessment in d.assessments.all():
                        if property.assessments.filter(land_value=assessment.land_value, full_value=assessment.full_value, year=assessment.year).count() > 0:
                            assessment.delete()
                        else:
                            assessment.property = property
                            assessment.save()

                    d.residence.get().delete()
                    d.land.get().delete()
                    d.save()
                    delete_list.append(d)

                print('duplicates removed.')

            property.save()

        delete_count = len(delete_list)

        for p in delete_list:
            print('deleting ' + str(delete_list.index(p)) + ' of ' + str(delete_count) + '...')
            p.delete()

        return delete_count
