# Generated by Django 3.2.14 on 2022-08-28 23:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tactb', '0012_defaultact'),
    ]

    operations = [
        migrations.CreateModel(
            name='GLDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField()),
                ('line_uid', models.UUIDField()),
                ('document_type', models.CharField(default='', max_length=50)),
                ('document_no', models.CharField(default='', max_length=50)),
                ('line_number', models.IntegerField(default=0)),
                ('item_code', models.CharField(default='', max_length=50)),
                ('item_description', models.CharField(default='', max_length=200)),
                ('quantity', models.IntegerField(default=1)),
                ('bal_quantity', models.FloatField(default=0)),
                ('unit_price', models.FloatField(default=0)),
                ('stock_uom', models.CharField(default='', max_length=50)),
                ('selling_uom', models.CharField(default='', max_length=50)),
                ('trx_curr_amount', models.FloatField(default=0)),
                ('base_curr_amount', models.FloatField(default=0)),
                ('taxable_yn', models.CharField(default='n', max_length=50)),
                ('tax_code1', models.CharField(default='', max_length=50)),
                ('tax_code2', models.CharField(default='', max_length=50)),
                ('tax_code3', models.CharField(default='', max_length=50)),
                ('tax_pecent1', models.FloatField(default=0)),
                ('tax_pecent2', models.FloatField(default=0)),
                ('tax_pecent3', models.FloatField(default=0)),
                ('discount_percent', models.FloatField(default=0)),
                ('location_code', models.CharField(default='', max_length=50)),
                ('account_code', models.CharField(default='', max_length=50)),
                ('db_cr', models.CharField(default='db', max_length=2)),
                ('trx_sign', models.IntegerField(default=1)),
                ('ref_document_typ', models.CharField(default='', max_length=50)),
                ('ref_document_no', models.CharField(default='', max_length=50)),
                ('tag_header_yn', models.CharField(default='d', max_length=1)),
                ('party_code', models.CharField(default='', max_length=50)),
                ('ref_trx_curr', models.CharField(default='', max_length=3)),
                ('date_trans', models.DateField(default=datetime.datetime(2022, 8, 29, 7, 21, 33, 168388))),
                ('tax_amount_forex1', models.FloatField(default=0)),
                ('tax_amount_forex2', models.FloatField(default=0)),
                ('tax_amount_forex3', models.FloatField(default=0)),
                ('tax_amount_local1', models.FloatField(default=0)),
                ('tax_amount_local2', models.FloatField(default=0)),
                ('tax_amount_local3', models.FloatField(default=0)),
                ('extnamount_forex', models.FloatField(default=0)),
                ('extnamount_local', models.FloatField(default=0)),
                ('remarks', models.TextField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='GLHeader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField()),
                ('document_type', models.CharField(default='', max_length=50)),
                ('document_no', models.CharField(default='', max_length=50)),
                ('date_trans', models.DateField(default=datetime.datetime(2022, 8, 29, 7, 21, 33, 168388))),
                ('document_reference', models.CharField(default='', max_length=50)),
                ('additional_reference', models.CharField(default='', max_length=50)),
                ('usercode', models.CharField(default='', max_length=50)),
                ('remarks', models.TextField(default='')),
                ('document_status', models.CharField(default='a', max_length=50)),
                ('party_code', models.CharField(default='', max_length=50)),
                ('party_name', models.CharField(default='', max_length=200)),
                ('currency_code', models.CharField(default='', max_length=3)),
                ('amount_local', models.FloatField(default=0, max_length=50)),
                ('amount_forex', models.FloatField(default=0, max_length=50)),
                ('ex_rate', models.FloatField(default=1, max_length=50)),
                ('tax_amount1', models.FloatField(default=0, max_length=50)),
                ('tax_amount2', models.FloatField(default=0, max_length=50)),
                ('tax_amount3', models.FloatField(default=0, max_length=50)),
                ('nontax_amount1', models.FloatField(default=0, max_length=50)),
                ('nontax_amount2', models.FloatField(default=0, max_length=50)),
                ('nontax_amount3', models.FloatField(default=0, max_length=50)),
                ('valid_till', models.DateField(default=datetime.datetime(2022, 8, 29, 7, 21, 33, 168388))),
                ('term_code', models.CharField(default='', max_length=50)),
                ('term_days', models.IntegerField(default=0)),
                ('trx_sign', models.IntegerField(default=1)),
                ('act_code', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='GLSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField()),
                ('reference_no', models.CharField(default='', max_length=50)),
                ('reference_uid', models.UUIDField()),
                ('act_year', models.IntegerField(default=1)),
                ('act_period', models.IntegerField(default=1)),
                ('document_type', models.CharField(default='', max_length=50)),
                ('document_no', models.CharField(default='', max_length=50)),
                ('document_date', models.DateField(default=datetime.datetime(2022, 8, 29, 7, 21, 33, 168388))),
                ('serial_no', models.IntegerField(default=1)),
                ('act_code', models.CharField(default='', max_length=50)),
                ('curr_code', models.CharField(default='', max_length=3)),
                ('sign', models.IntegerField(default=1)),
                ('amount_local', models.FloatField(default=0)),
                ('amount_forex', models.FloatField(default=0)),
                ('entered_by', models.CharField(default='', max_length=50)),
                ('enterd_date', models.DateField(default=datetime.datetime(2022, 8, 29, 7, 21, 33, 168388))),
                ('party_code', models.CharField(default='', max_length=50)),
                ('party_name', models.CharField(default='', max_length=200)),
                ('item_code', models.CharField(default='', max_length=50)),
                ('item_description', models.CharField(default='', max_length=200)),
                ('remarks', models.TextField(default='', max_length=50)),
                ('trans_mode', models.CharField(default='', max_length=50)),
                ('offset_act', models.CharField(default='', max_length=50)),
                ('location_code', models.CharField(default='', max_length=50)),
                ('entry_type', models.CharField(default='', max_length=50)),
            ],
        ),
    ]
