# Generated by Django 4.0.4 on 2022-05-18 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DdosTool', '0002_keypairs_remove_commands_bandwidth_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devices',
            name='keyPair',
        ),
    ]