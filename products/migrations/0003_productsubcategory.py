# Generated by Django 3.0.8 on 2021-02-22 03:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210216_1817'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductSubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.ProductCategory')),
            ],
        ),
    ]