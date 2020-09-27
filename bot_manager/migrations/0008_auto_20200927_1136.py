# Generated by Django 3.1.1 on 2020-09-27 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_manager', '0007_auto_20200927_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='action',
            field=models.CharField(choices=[('stop_campaign', 'Stop campaign'), ('Start campaign', 'Start campaign'), ('Add landing to BL', 'Add landing to BL'), ('Add landing to WL', 'Add landing to WL')], max_length=128, verbose_name='Action'),
        ),
    ]
