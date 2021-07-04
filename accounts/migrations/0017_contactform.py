# Generated by Django 3.0.8 on 2021-06-29 06:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20210407_1809'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=13, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+99999999", regex='^\\+?1?\\d{9,14}$')])),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('message', models.CharField(blank=True, max_length=1000)),
            ],
        ),
    ]