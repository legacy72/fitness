# Generated by Django 3.0.4 on 2020-06-01 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200520_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='img',
            field=models.TextField(blank=True, null=True, verbose_name='Картинка'),
        ),
    ]