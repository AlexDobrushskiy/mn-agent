# Generated by Django 3.0.3 on 2020-12-11 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masternode',
            name='address',
            field=models.CharField(max_length=35, null=True),
        ),
        migrations.AlterField(
            model_name='masternode',
            name='balance',
            field=models.IntegerField(null=True),
        ),
    ]
