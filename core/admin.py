from django.contrib import admin

from core.models import Client, City


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'is_active', 'list_cities', 'visa_sub_category')
    list_filter = ('cities',)

    def list_cities(self, obj):
        return ", ".join([related_obj.title for related_obj in obj.cities.all()])

    list_cities.short_description = 'Cities'


@admin.register(City)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')