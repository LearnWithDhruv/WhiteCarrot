from django.db import models

class GoogleCredentials(models.Model):
    user_email = models.EmailField(unique=True, default="")
    refresh_token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_email
