# Generated by Django 3.0.3 on 2020-02-18 02:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0006_auto_20200218_1023'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='parant',
            new_name='parent',
        ),
    ]
