# Generated by Django 3.0.4 on 2020-06-09 16:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_authcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authcode',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 9, 22, 6, 5, 543355, tzinfo=utc), verbose_name='Дата окончания действия'),
        ),
    ]
