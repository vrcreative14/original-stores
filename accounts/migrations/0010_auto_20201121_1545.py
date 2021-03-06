# Generated by Django 3.1.2 on 2020-11-21 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='phoneotp',
            name='forgot',
            field=models.BooleanField(default=False, help_text='only true for forgot password'),
        ),
        migrations.AddField(
            model_name='phoneotp',
            name='forgot_logged',
            field=models.BooleanField(default=False, help_text='Only true if validdate otp forgot get successful'),
        ),
        migrations.AddField(
            model_name='phoneotp',
            name='logged',
            field=models.BooleanField(default=False, help_text='If otp verification got successful'),
        ),
    ]
