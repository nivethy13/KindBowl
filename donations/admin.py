from django.contrib import admin
from .models import FoodDonation, DonationHistory

@admin.register(FoodDonation)
class FoodDonationAdmin(admin.ModelAdmin):
    list_display = ('food_type', 'quantity', 'unit', 'donor', 'status', 'created_at')
    list_filter = ('food_type', 'status', 'created_at')
    search_fields = ('donor__username', 'description')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

@admin.register(DonationHistory)
class DonationHistoryAdmin(admin.ModelAdmin):
    list_display = ('donation', 'ngo', 'status', 'accepted_at')
    list_filter = ('status', 'accepted_at')
    search_fields = ('donation__donor__username', 'ngo__organization_name')
    readonly_fields = ('accepted_at',)
    date_hierarchy = 'accepted_at'
