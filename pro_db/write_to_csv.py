import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'pro_db.settings'

import django

django.setup()

import properties.models as mods
import csv

all_properties = {}
count = 0
for t in mods.TaxInformation.objects.filter(year_summaries__gross_tax__gt=0):
    if t.total_gross_taxes() > 5000:
        count += 1
        all_properties[t.property.street_line()] = t.property
        print(count)

with open('result.csv', 'w') as f:
    writer = csv.writer(f, dialect='excel')
    count = 0
    all_sections = []
    for property in all_properties.values():
        section = []
        count += 1
        section.append([property.street_line(), '---', property.owner.name])
        section.append(['Taxes:', 'Year', 'Amount Due'])

        for y in property.tax_info.get().year_summaries.all():
            section.append(['', y.year, y.gross_tax])

        section.append(['Total', '--', property.tax_info.get().total_gross_taxes()])

        if section not in all_sections:
            all_sections.append(section)

    for s in all_sections:
        for line in s:
            writer.writerow(line)

    print(count)