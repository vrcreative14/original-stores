# Generated by Django 3.1.2 on 2021-02-04 03:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0015_auto_20210131_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='store_manager',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='stores.storemanager'),
        ),
    ]