# Generated by Django 3.1.4 on 2021-01-13 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_mnconnection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chunk',
            name='chunk_id',
            field=models.CharField(max_length=256),
        ),
    ]
