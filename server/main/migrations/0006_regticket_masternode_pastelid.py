# Generated by Django 3.1.4 on 2020-12-23 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_regticket_masternode_pastelid'),
    ]

    operations = [
        migrations.AddField(
            model_name='regticket',
            name='masternode_pastelid',
            field=models.ForeignKey(default=1986, on_delete=django.db.models.deletion.CASCADE, to='main.masternode', to_field='pastelID'),
            preserve_default=False,
        ),
    ]