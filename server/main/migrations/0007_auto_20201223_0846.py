# Generated by Django 3.1.4 on 2020-12-23 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_regticket_masternode_pastelid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regticket',
            name='masternode_pastelid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.masternode', to_field='pastelID'),
        ),
    ]