# Generated by Django 3.1.5 on 2021-01-27 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_manager', '0064_auto_20210126_0539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='action',
            field=models.SmallIntegerField(choices=[(2, 'Stop campaign'), (1, 'Play campaign'), (3, 'Add zone to black list'), (4, 'Add zone to white list')], verbose_name='Target action'),
        ),
    ]
