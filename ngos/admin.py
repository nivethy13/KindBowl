from django.contrib import admin
from .models import NGOProfile

@admin.register(NGOProfile)
class NGOProfileAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'user', 'is_verified', 'capacity', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('organization_name', 'user__username', 'registration_number')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
