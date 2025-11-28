from django.contrib import admin
from .models import CompanyProfile, JobPosting, JobApplication

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'industry', 'location', 'is_verified', 'created_at')
    list_filter = ('industry', 'is_verified', 'created_at')
    search_fields = ('company_name', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'job_type', 'experience_level', 'location', 'is_active', 'views_count', 'likes_count', 'saves_count')
    list_filter = ('job_type', 'experience_level', 'is_active', 'created_at')
    search_fields = ('title', 'company__company_name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'views_count', 'likes_count', 'saves_count')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('job__title', 'applicant__username', 'applicant__email')
    readonly_fields = ('applied_at',)