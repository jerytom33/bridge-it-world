from django.db import models
from django.contrib.auth.models import User

class RoleUser(models.Model):
    objects = models.Manager()  # Type hint for static analysis
    
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('guide', 'Guide'),
        ('company', 'Company'),
        ('admin', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    is_approved = models.BooleanField(default=False)  # type: ignore
    is_blocked = models.BooleanField(default=False)  # type: ignore
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"  # type: ignore

    class Meta:
        db_table = 'admin_panel_roleuser'