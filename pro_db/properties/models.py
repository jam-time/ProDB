from django.db import models
import jsonfield


class SourceSiteGroup(models.Model):
    origin_url = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    table_page = models.IntegerField(default=0)

    def generate_request_data(self, raw_html, data=dict):
        import re

        capture_group = r'(.*)'
        wildcard = r'[\w\W]*'
        pattern = ''

        for p in self.data_patterns:
            if pattern != '':
                pattern += wildcard
            pattern += p['start'] + capture_group + p['end']

        parsed_response = re.search(pattern, raw_html)
        groups = list(parsed_response.groups())

        for i in range(len(groups)):
            try:
                data[self.data_patterns[i]['name']] = groups[i]
            except TypeError:
                return None

        return data

    def update_session(self, session):
        self.session_headers = session.headers
        self.session_params = session.params


class SourceSite(models.Model):
    origin = models.ForeignKey('SourceSiteGroup', on_delete=models.CASCADE, related_name='sites')
    source = models.ForeignKey('self', on_delete=models.CASCADE, related_name='branches', null=True)
    url = models.CharField(max_length=255)

    def __str__(self):
        return ' - '.join([str(self.origin.name), str(self.url)])


class Owner(models.Model):
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Property(models.Model):
    owners = models.ManyToManyField('Owner', related_name='properties', default=None)
    source_site_groups = models.ManyToManyField('SourceSiteGroup', related_name='properties', default=None)
    street = models.CharField(max_length=255)
    street_num = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    raw_text = models.TextField(default='')

    def street_line(self):
        return f'{self.street_num} {self.street}'

    def unit(self):
        return self.residence.unit

    def city_line(self):
        return f'{self.city}, {self.state} {self.postal_code}'

    def full_address(self):
        if self.unit() is not None and self.unit() != '':
            lines = [self.street_line(), self.unit(), self.city_line(), self.country]
        else:
            lines = [self.street_line(), self.city_line(), self.country]

        return '\n'.join(lines)

    def total_taxes_due(self):
        try:
            return self.tax_info.objects.aggregate(models.Sum('gross_amount'))
        except:
            return 0

    def __str__(self):
        return ' '.join([self.street_num, self.street])


class TaxInformation(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE, related_name='tax_info')
    raw_text = models.TextField()

    def total_gross_taxes(self):
        try:
            return self.year_summaries.aggregate(models.Sum('gross_tax'))['gross_tax__sum']
        except:
            return 0

    def total_base_taxes(self):
        try:
            return self.year_summaries.aggregate(models.Sum('base_tax'))['base_tax__sum']
        except:
            return 0

    def total_penalty_fees(self):
        try:
            return self.year_summaries.aggregate(models.Sum('penalty_fees'))['penalty_fees__sum']
        except:
            return 0

    def total_other_fees(self):
        try:
            return self.year_summaries.aggregate(models.Sum('other_fees'))['other_fees__sum']
        except:
            return 0


class TaxYearSummary(models.Model):
    tax_info = models.ForeignKey('TaxInformation', on_delete=models.CASCADE, related_name='year_summaries')
    gross_tax = models.FloatField(default=0.0)
    base_tax = models.FloatField(default=0.0)
    penalty_fees = models.FloatField(default=0.0)
    other_fees = models.FloatField(default=0.0)
    year = models.IntegerField(default=None, null=True)


class Assessment(models.Model):
    MONTHS = (
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December')
    )
    property = models.ForeignKey('Property', on_delete=models.CASCADE, related_name='assessments')
    land_value = models.FloatField()
    full_value = models.FloatField()
    year = models.IntegerField()
    month = models.IntegerField(choices=MONTHS)
    day = models.IntegerField()

    def __str__(self):
        return f'{self.id}: ${self.full_value}'


class ExternalID(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE, related_name='external_ids')
    source = models.ForeignKey('SourceSiteGroup', on_delete=models.CASCADE, related_name='external_ids', null=True)
    type = models.CharField(max_length=255, default='id')
    id_external = models.CharField(max_length=255)

    def __str__(self):
        return f'ExID: {self.source} {self.id_external}'


class Residence(models.Model):
    property = models.OneToOneField('Property', on_delete=models.CASCADE, primary_key=True, related_name='residence')
    area = models.CharField(max_length=255)
    bed_count = models.IntegerField(default=1)
    full_bath_count = models.IntegerField(default=1)
    half_bath_count = models.IntegerField(default=0)
    bath_count = models.FloatField(default=1)
    unit = models.CharField(max_length=255)
    stories = models.IntegerField(default=1)
    basement = models.BooleanField(default=False)
    pool = models.BooleanField(default=False)
    garage_capacity = models.IntegerField(default=0)
    fireplace_count = models.IntegerField(default=0)
    year_built = models.IntegerField(default=0)
    kitchen_count = models.IntegerField(default=1)
    sewer = models.CharField(max_length=255)
    utilities = models.CharField(max_length=255)
    fuel = models.CharField(max_length=255)
    water = models.CharField(max_length=255)
    heat = models.CharField(max_length=255)
    central_air = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)
    grade = models.CharField(max_length=255)
    zoning_code = models.CharField(max_length=255)

    def __str__(self):
        return self.property.__str__()


class Land(models.Model):
    property = models.OneToOneField('Property', on_delete=models.CASCADE, primary_key=True, related_name='land')
    area = models.CharField(max_length=255)

    def __str__(self):
        return self.property.__str__()
