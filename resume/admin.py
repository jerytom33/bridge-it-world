from django.contrib import admin
from .models import ResumeAnalysis

@admin.register(ResumeAnalysis)
class ResumeAnalysisAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'candidate_name', 'candidate_level', 
                    'predicted_field', 'resume_score', 'created_at']
    list_filter = ['candidate_level', 'predicted_field', 'created_at']
    search_fields = ['user__username', 'candidate_name', 'candidate_email']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'pdf_file')
        }),
        ('Candidate Details', {
            'fields': ('candidate_name', 'candidate_email', 'candidate_phone')
        }),
        ('Analysis Results', {
            'fields': ('candidate_level', 'predicted_field', 'resume_score', 
                      'detected_skills', 'recommended_skills', 'recommended_courses',
                      'score_breakdown')
        }),
        ('AI Responses', {
            'fields': ('gemini_response', 'analyzer_response'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )
