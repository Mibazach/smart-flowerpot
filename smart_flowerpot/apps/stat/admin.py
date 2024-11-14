from django.contrib import admin
from .models import Flowerpot, EnvironmentData

@admin.register(Flowerpot)
class FlowerpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'created_at', 'updated_at')
    search_fields = ('name', 'location')
    list_filter = ('created_at', 'updated_at')

@admin.register(EnvironmentData)
class EnvironmentDataAdmin(admin.ModelAdmin):
    list_display = ('flowerpot', 'temperature', 'moisture', 'ph_level', 'light_level', 'humidity', 'created_at')
    search_fields = ('flowerpot__name',)
    list_filter = ('created_at', 'flowerpot')
    readonly_fields = ('hash',)
