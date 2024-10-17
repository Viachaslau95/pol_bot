# Generated by Django 4.2.4 on 2023-10-06 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_client_visa_sub_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='visa_sub_category',
            field=models.CharField(choices=[('Driver D-visa', 'Driver D-visa'), ('Karta Polaka D-visa', 'Karta Polaka D-visa'), ('Other D-visa', 'Other D-visa'), ('Postal D-visa', 'Postal D-visa'), ('Work D-visa', 'Work D-visa'), ('D - National', 'D - National'), ('D - Nacional', 'D - Nacional'), ('D - Inne', 'D - Inne'), ('D - National Visa', 'D - National Visa'), ('D - Student', 'D - Student'), ('D - Stydent', 'D - Stydent'), ('D - Studenci', 'D - Studenci'), ('D - Student Visa', 'D - Student Visa'), ('D - Uczen', 'D - Uczen'), ('D - Uchenik', 'D - Uchenik'), ('D - Uczniowie', 'D - Uczniowie'), ('D - Uczen Visa', 'D - Uczen Visa'), ('PBH D-visa', 'PBH D-visa'), ('D - PBH', 'D - PBH'), ('D - PBH Visa', 'D - PBH Visa'), ('Krajowa', 'Krajowa'), ('PRACA', 'PRACA'), ('Natsionalnaya Viza', 'Natsionalnaya Viza'), ('Nacyjanalnaya', 'Nacyjanalnaya'), ('Studenckaya', 'Studenckaya'), ('Studencheskaya Viza', 'Studencheskaya Viza'), ('Other C visa', 'Other C visa'), ('USA Embassy, KP exam/odbior C-Visa', 'USA Embassy, KP exam/odbior C-Visa'), ('Tourism C-visa', 'Tourism C-visa'), ('C - Biznes', 'C - Biznes'), ('C - Business Visa', 'C - Business Visa'), ('C - Culture Visa', 'C - Culture Visa'), ('C - Kultura', 'C - Kultura'), ('C - Odwiedziny', 'C - Odwiedziny'), ('C - Visit Visa', 'C - Visit Visa'), ('C - Schengen', 'C - Schengen'), ('Szengen', 'Szengen'), ('Schengenskaya - Wojewodskoe priglashenie', 'Schengenskaya - Wojewodskoe priglashenie'), ('Schengenskaya Viza', 'Schengenskaya Viza')], help_text='Be very careful!\nD - PBH Visa and PBH D-Visa are for different cities!!!', max_length=50),
        ),
    ]
