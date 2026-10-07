from django.contrib import admin
from .models import Customer, Lead, Opportunity, FollowUp, AuditLog

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_code', 'customer_name', 'email', 'phone', 'status', 'created_date')
    search_fields = ('customer_name', 'email', 'phone', 'company_name')

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('lead_code', 'lead_name', 'email', 'phone', 'status', 'expected_value')
    list_filter = ('status', 'source')
    search_fields = ('lead_name', 'company_name')

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('opportunity_name', 'amount', 'stage', 'probability', 'expected_close_date', 'status')
    list_filter = ('stage', 'status')

@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    list_display = ('follow_up_type', 'follow_up_date', 'status', 'assigned_to')
    list_filter = ('status', 'follow_up_type')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'entity_name', 'record_id', 'created_date')
    readonly_fields = ('created_date',)