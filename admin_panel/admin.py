from django.contrib import admin
from .models import RoleUser

@admin.register(RoleUser)
class RoleUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'is_approved', 'is_blocked', 'created_at')
    list_filter = ('role', 'is_approved', 'is_blocked')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
