# Generated by Django 3.2.14 on 2022-08-03 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tactb', '0009_partyinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='partyinfo',
            name='partyName2',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
