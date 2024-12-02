from django.contrib import admin
from .models import Flowerpot, EnvironmentData

@admin.register(Flowerpot)
class FlowerpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug','location', 'created_at', 'updated_at')
    search_fields = ('name', 'location')
    list_filter = ('created_at', 'updated_at')

@admin.register(EnvironmentData)
class EnvironmentDataAdmin(admin.ModelAdmin):
    list_display = ('flowerpot_slug', 'flowerpot_name', 'soil_moisture', 'air_humidity', 'temperature', 'created_at', 'hash')
    search_fields = ('flowerpot__name', 'flowerpot__slug')
    list_filter = ('created_at', 'flowerpot__name', 'flowerpot__slug')
    readonly_fields = ('hash',)

    def flowerpot_slug(self, obj):
        return obj.flowerpot.slug
    flowerpot_slug.short_description = 'Flowerpot Slug'

    def flowerpot_name(self, obj):
        return obj.flowerpot.name
    flowerpot_name.short_description = 'Flowerpot Name'