from django.contrib import admin
from .models import Member
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display=("membership_number","full_name","tier","status","issue_date","expiry_date")
    list_filter=("tier","status","payment_method"); search_fields=("membership_number","full_name","phone","email"); readonly_fields=("membership_number","created_at")
