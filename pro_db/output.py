import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'pro_db.settings'

import django

django.setup()

import properties.models as mods
import re

count = 0
for p in mods.Property.objects.filter():
    count += 1
    print(str(count) + '...')

    t = p.tax_info.get()
    raw = t.raw_text

    year = re.compile(r'etaxTemplateForm:payments_:.:year." class="outputText">(.*)</span>')
    base_amount = re.compile(r'etaxTemplateForm:payments_:.:taxesDueTxt" class="outputText">\$(.*)</span>')
    penalty_fees = re.compile(r'etaxTemplateForm:payments_:.:pniDueTxt" class="outputText">\$(.*)</span>')
    other_fees = re.compile(r'etaxTemplateForm:payments_:.:feeDueTxt" class="outputText">\$(.*)</span>')
    gross_amount = re.compile(r'etaxTemplateForm:payments_:.:amountDue2" class="outputText">\$(.*)</span>')

    try:
        year_list = year.findall(raw)
    except:
        year_list = [2019]

    try:
        base_list = base_amount.findall(raw)
    except:
        base_list = [0]

    try:
        penalty_list = penalty_fees.findall(raw)
    except:
        penalty_list = [0]

    try:
        other_list = other_fees.findall(raw)
    except:
        other_list = [0]

    try:
        gross_list = gross_amount.findall(raw)
    except:
        gross_list = [0]

    if len(year_list) > 0:
        for i in range(len(year_list)):
            try:
                summary = t.year_summaries.get(year=int(year_list[i]))
            except:
                summary = t.year_summaries.create(year=int(year_list[i]))

            try:
                summary.gross_tax = float(gross_list[i].replace(',', ''))
            except:
                summary.save()

            try:
                summary.base_tax = float(base_list[i].replace(',', ''))
            except:
                summary.save()

            try:
                summary.penalty_fees = float(penalty_list[i].replace(',', ''))
            except:
                summary.save()

            try:
                summary.other_fees = float(other_list[i].replace(',', ''))
            except:
                summary.save()

            summary.save()

        t.save()

    print(p.full_address())
