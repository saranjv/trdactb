# Generated by Django 3.2.14 on 2022-07-27 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tactb', '0004_finyear'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finyear',
            name='compCode',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tactb.companyinfo'),
        ),
    ]
