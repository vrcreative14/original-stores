# Generated by Django 3.1.2 on 2020-12-03 12:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20201203_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='secondary_email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='seller',
            name='secondary_phone',
            field=models.CharField(blank=True, max_length=13, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+99999999", regex='^\\+?1?\\d{9,14}$')]),
        ),
    ]
