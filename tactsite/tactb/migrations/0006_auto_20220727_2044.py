# Generated by Django 3.2.14 on 2022-07-27 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tactb', '0005_alter_finyear_compcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='finyear',
            name='dateFrom5',
            field=models.DateField(default='2020-11-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='finyear',
            name='dateTo4',
            field=models.DateField(default='2020-11-01'),
            preserve_default=False,
        ),
    ]
