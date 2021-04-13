# Generated by Django 3.1.5 on 2021-03-29 14:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('bot_manager', '0078_auto_20210329_1452'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bot',
            name='campaigns_list',
        ),
        migrations.AddField(
            model_name='bot',
            name='campaigns_list',
            field=models.JSONField(default={},
                                   help_text='If campaign doesn\'t exist, you can create it here using "+".',
                                   verbose_name='Campaigns'),
            preserve_default=False,
        ),
    ]
