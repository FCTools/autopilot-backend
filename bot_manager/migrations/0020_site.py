# Generated by Django 3.1.1 on 2020-10-09 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_manager', '0019_auto_20201007_1639'),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='Site ID')),
                ('name', models.CharField(max_length=512, verbose_name='Name')),
            ],
        ),
    ]
