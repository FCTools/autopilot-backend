# Generated by Django 3.1.5 on 2021-01-29 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot_manager', '0070_auto_20210129_0627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='traffic_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bot_manager.trafficsource', verbose_name='Traffic source'),
        ),
    ]
