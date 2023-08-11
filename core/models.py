from django.db import models


class Client(models.Model):
    reg_email = models.CharField(max_length=120)
    reg_password = models.CharField(max_length=120)

    national_id = models.CharField(max_length=250, unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    gender = models.CharField(max_length=20, blank=True, null=True)
    passport_number = models.CharField(max_length=100)
    passport_expire_date = models.CharField(max_length=10)
    code_country = models.IntegerField(default=0)
    contact_number = models.IntegerField(default=0)
    admin_email = models.CharField(max_length=120)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.firstname}-{self.lastname}'
