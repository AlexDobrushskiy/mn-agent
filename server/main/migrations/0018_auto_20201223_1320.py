# Generated by Django 3.1.4 on 2020-12-23 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20201223_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chunk',
            name='mn_pastelid',
            field=models.CharField(default=1234555, max_length=86, unique=True),
            preserve_default=False,
        ),
    ]