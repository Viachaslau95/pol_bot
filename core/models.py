from django.db import models

from core.choices import GENDER_CHOICES, VISA_CHOICES, VISA_SUB_CHOICES


class Client(models.Model):
    reg_email = models.CharField(max_length=120)
    reg_password = models.CharField(max_length=120)

    national_id = models.CharField(max_length=250, unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    date_of_birth = models.CharField(max_length=12, help_text='format - 00/00/0000')
    gender = models.CharField(max_length=25, choices=GENDER_CHOICES)
    passport_number = models.CharField(max_length=100, help_text='format - mp1234567')
    passport_expire_date = models.CharField(max_length=10, help_text='format - 00112222')
    code_country = models.IntegerField(default=0, help_text='375')
    contact_number = models.IntegerField(default=0, help_text='9 digits')
    admin_email = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)

    cities = models.ManyToManyField(
        'City', blank=True, related_name='clients'
    )
    visa_type = models.CharField(max_length=50, choices=VISA_CHOICES)
    visa_sub_category = models.CharField(max_length=50, choices=VISA_SUB_CHOICES,
                                         help_text='Be very careful!\n'
                                                   'D - PBH Visa and PBH D-Visa are for different cities!!!'
                                         )

    def __str__(self):
        return f'{self.firstname}-{self.lastname}'


class City(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title
