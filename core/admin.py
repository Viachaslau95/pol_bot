from django.contrib import admin

from core.models import Client, City


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'is_active')


@admin.register(City)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')