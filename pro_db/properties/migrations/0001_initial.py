# Generated by Django 2.2.6 on 2019-11-03 04:54

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=255)),
                ('street_num', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='properties.Owner')),
            ],
        ),
        migrations.CreateModel(
            name='SourceSiteGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_url', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('session_headers', jsonfield.fields.JSONField(default=dict)),
                ('session_params', jsonfield.fields.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='Land',
            fields=[
                ('property', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='land', serialize=False, to='properties.Property')),
                ('area', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Residence',
            fields=[
                ('property', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='residence', serialize=False, to='properties.Property')),
                ('area', models.CharField(max_length=255)),
                ('bed_count', models.IntegerField(default=1)),
                ('full_bath_count', models.IntegerField(default=1)),
                ('half_bath_count', models.IntegerField(default=0)),
                ('bath_count', models.FloatField(default=1)),
                ('unit', models.CharField(max_length=255)),
                ('stories', models.IntegerField()),
                ('basement', models.BooleanField(default=False)),
                ('pool', models.BooleanField(default=False)),
                ('garage_capacity', models.IntegerField(default=0)),
                ('fireplace_count', models.IntegerField(default=0)),
                ('year_built', models.IntegerField()),
                ('kitchen_count', models.IntegerField(default=1)),
                ('sewer', models.CharField(max_length=255)),
                ('utilities', models.CharField(max_length=255)),
                ('fuel', models.CharField(max_length=255)),
                ('water', models.CharField(max_length=255)),
                ('heat', models.CharField(max_length=255)),
                ('central_air', models.CharField(max_length=255)),
                ('condition', models.CharField(max_length=255)),
                ('grade', models.CharField(max_length=255)),
                ('zoning_code', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TaxInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raw_text', models.TextField()),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tax_info', to='properties.Property')),
            ],
        ),
        migrations.CreateModel(
            name='SourceSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
                ('data_patterns', jsonfield.fields.JSONField(default=dict)),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sites', to='properties.SourceSiteGroup')),
                ('source', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='branches', to='properties.SourceSite')),
            ],
        ),
        migrations.CreateModel(
            name='ExternalID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_external', models.CharField(max_length=255)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='external_ids', to='properties.Property')),
                ('source', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='external_ids', to='properties.SourceSiteGroup')),
            ],
        ),
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('land_value', models.FloatField()),
                ('full_value', models.FloatField()),
                ('year', models.IntegerField()),
                ('month', models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')])),
                ('day', models.IntegerField()),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessments', to='properties.Property')),
            ],
        ),
    ]