# Generated by Django 3.0.3 on 2020-12-11 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Masternode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=15, unique=True)),
                ('address', models.CharField(max_length=35)),
                ('balance', models.IntegerField()),
            ],
        ),
    ]
