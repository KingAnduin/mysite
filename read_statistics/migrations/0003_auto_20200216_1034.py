# Generated by Django 3.0.3 on 2020-02-16 02:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('read_statistics', '0002_readdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readdetail',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 2, 16, 2, 34, 56, 285793, tzinfo=utc)),
        ),
    ]