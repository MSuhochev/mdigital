from django.db import models
from django.utils import timezone


class Resume(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    resume_file = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(max_length=200, blank=True, null=True)
    date_sent = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
