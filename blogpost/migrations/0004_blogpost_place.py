# Generated by Django 3.0.8 on 2021-04-11 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogpost', '0003_auto_20210411_2245'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='place',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]