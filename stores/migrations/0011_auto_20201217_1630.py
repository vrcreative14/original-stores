# Generated by Django 3.1.2 on 2020-12-17 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0010_auto_20201217_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storedetails',
            name='popularity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stores.popularity'),
        ),
    ]
