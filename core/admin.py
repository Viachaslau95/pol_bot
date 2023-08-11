from django.contrib import admin

from core.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'reg_email', 'reg_password')
