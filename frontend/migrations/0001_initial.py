# Generated by Django 3.0.8 on 2021-06-12 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HindiContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_name', models.CharField(max_length=100)),
                ('sub_heading', models.CharField(max_length=500)),
                ('content', models.CharField(max_length=10000)),
            ],
        ),
    ]
