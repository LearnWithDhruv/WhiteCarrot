from django.db import models

class GoogleCredentials(models.Model):
    user_email = models.EmailField(unique=True, default="")
    refresh_token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_email

class CalendarEvent(models.Model):
    title = models.CharField(max_length=255)  
    location = models.CharField(max_length=255, blank=True, null=True)  
    start_time = models.DateTimeField()  
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.title
