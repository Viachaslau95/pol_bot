# Generated by Django 4.2.4 on 2023-08-21 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_client_visa_sub_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='visa_sub_category',
            field=models.CharField(choices=[('Driver D-visa', 'Driver D-visa'), ('Karta Polaka D-visa', 'Karta Polaka D-visa'), ('Other D-visa', 'Other D-visa'), ('Postal D-visa', 'Postal D-visa'), ('Work D-visa', 'Work D-visa'), ('D - National', 'D - National'), ('D - Inne', 'D - Inne'), ('D - National Visa', 'D - National Visa'), ('D - Student', 'D - Student'), ('D - Studenci', 'D - Studenci'), ('D - Student Visa', 'D - Student Visa'), ('D - Uczen', 'D - Uczen'), ('D - Uczniowie', 'D - Uczniowie'), ('D - Uczen Visa', 'D - Uczen Visa'), ('PBH D-visa', 'PBH D-visa'), ('D - PBH', 'D - PBH'), ('D - PBH Visa', 'D - PBH Visa')], help_text='Be very careful!\nD - PBH Visa and PBH D-Visa are for different cities!!!', max_length=50),
        ),
    ]
