# Generated by Django 4.2.4 on 2023-08-11 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_client_admin_email_client_code_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='national_id',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]
