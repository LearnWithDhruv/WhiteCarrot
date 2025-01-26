from google.oauth2 import id_token
from google.auth.transport import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import time, logging
from .models import GoogleCredentials
from google.auth.transport.requests import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CalendarEvent
from .serializers import CalendarEventSerializer
logger = logging.getLogger(__name__)

class GoogleLoginView(APIView):
    def post(self, request):
        logger.info(f"Request data: {request.data}")

        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_OAUTH_CLIENT_ID)

            user_email = idinfo.get('email')
            user_name = idinfo.get('name')

            # Log success
            logger.info(f"User authenticated: {user_email}")

            # Return success response
            return Response({'message': 'Logged in successfully', 'email': user_email, 'name': user_name}, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.error(f"Token verification failed: {str(e)}")
            return Response({'error': 'Invalid token', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CalendarEventsView(APIView):
    
    def get(self, request):
        
        try:
            events = CalendarEvent.objects.all()
            serializer = CalendarEventSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Failed to fetch events', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
       
        try:
            serializer = CalendarEventSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Event added successfully'}, status=status.HTTP_201_CREATED)
            return Response({'error': 'Invalid data', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Failed to add event', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
