# Generated by Django 3.1.5 on 2021-01-13 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot_manager', '0051_auto_20210113_1120'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bot',
            old_name='crontab_salt',
            new_name='crontab_comment',
        ),
    ]
