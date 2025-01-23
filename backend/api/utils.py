import requests
from datetime import datetime, timedelta
from django.conf import settings
from .models import GoogleCredentials

def refresh_access_token(user):
    credentials = GoogleCredentials.objects.get(user=user)
    if datetime.utcnow() >= credentials.token_expiry:
        data = {
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
            "refresh_token": credentials.refresh_token,
            "grant_type": "refresh_token",
        }
        response = requests.post("https://oauth2.googleapis.com/token", data=data).json()
        credentials.access_token = response["access_token"]
        credentials.token_expiry = datetime.utcnow() + timedelta(seconds=response["expires_in"])
        credentials.save()
    return credentials.access_token
