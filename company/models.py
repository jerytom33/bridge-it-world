from django.db import models
from django.contrib.auth.models import User
from feed.models import Post

class CompanyProfile(models.Model):
    objects = models.Manager()  # Type hint for static analysis
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    description = models.TextField()
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True)
    industry = models.CharField(max_length=100)
    established = models.IntegerField(null=True, blank=True)
    employee_count = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=15, blank=True)
    is_verified = models.BooleanField(default=False)  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.company_name)

class JobPosting(models.Model):
    objects = models.Manager()  # Type hint for static analysis
    
    JOB_TYPES = [
        ('fulltime', 'Full Time'),
        ('parttime', 'Part Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
    ]
    
    EXPERIENCE_LEVELS = [
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('intern', 'Intern'),
    ]
    
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVELS)
    location = models.CharField(max_length=100)
    salary_range = models.CharField(max_length=100, blank=True)
    application_deadline = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Stats
    views_count = models.IntegerField(default=0)  # type: ignore
    likes_count = models.IntegerField(default=0)  # type: ignore
    saves_count = models.IntegerField(default=0)  # type: ignore

    def __str__(self):
        return f"{self.title} at {self.company.company_name}"  # type: ignore

class JobApplication(models.Model):
    objects = models.Manager()  # Type hint for static analysis
    
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='job_applications/', blank=True)
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('applied', 'Applied'),
        ('reviewed', 'Reviewed'),
        ('interview', 'Interview Scheduled'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], default='applied')

    def __str__(self):
        return f"{self.applicant.username} applied for {self.job.title}"  # type: ignore


class CompanyExam(models.Model):
    """Model for company-specific exams that can appear in Upcoming Exams section"""
    objects = models.Manager()  # Type hint for static analysis
    
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='exams')
    title = models.CharField(max_length=200)
    description = models.TextField()
    exam_date = models.DateField()
    registration_deadline = models.DateField()
    level = models.CharField(max_length=20, choices=[
        ('10', '10th'),
        ('12', '12th'),
        ('ug', 'UG'),
        ('pg', 'PG'),
    ])
    link = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} by {self.company.company_name}"


class CompanyBootcamp(models.Model):
    """Model for company-specific bootcamps/training programs that can appear in Trending Courses section"""
    objects = models.Manager()  # Type hint for static analysis
    
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='bootcamps')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    duration = models.CharField(max_length=50)  # e.g., "6 weeks", "3 months"
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    link = models.URLField(blank=True)
    is_certified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} by {self.company.company_name}"