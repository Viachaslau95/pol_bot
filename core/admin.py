from django.contrib import admin

from core.models import Client, City


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('lastname', 'is_active', 'list_cities', 'visa_type', 'visa_sub_category')
    list_filter = ('cities',)
    list_editable = ('is_active',)

    def list_cities(self, obj):
        return ", ".join([related_obj.title for related_obj in obj.cities.all()])

    def edit_is_active(self, obj):
        return obj.is_active


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')