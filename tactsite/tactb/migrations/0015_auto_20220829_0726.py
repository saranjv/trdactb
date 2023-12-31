# Generated by Django 3.2.14 on 2022-08-28 23:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tactb', '0014_auto_20220829_0726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gldetail',
            name='date_trans',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='glheader',
            name='date_trans',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='glheader',
            name='valid_till',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='glsummary',
            name='document_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='glsummary',
            name='enterd_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
