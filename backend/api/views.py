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
            user_credentials = GoogleCredentials.objects.get(email=request.user.email)
            
            credentials = Credentials(
                None,
                refresh_token=user_credentials.refresh_token,
                token_uri='https://oauth2.googleapis.com/token',
                client_id=settings.GOOGLE_OAUTH_CLIENT_ID,
                client_secret=settings.GOOGLE_OAUTH_CLIENT_SECRET,
            )
            credentials.refresh(Request())
            
            service = build('calendar', 'v3', credentials=credentials)
            
            events_result = service.events().list(calendarId='primary', maxResults=10).execute()
            events = events_result.get('items', [])
            
            formatted_events = [{
                'summary': event.get('summary', ''),
                'dateTime': event.get('start', {}).get('dateTime') or event.get('start', {}).get('date'),
                'location': event.get('location', '') or None
            } for event in events]
            
            return Response(formatted_events)
        
        except GoogleCredentials.DoesNotExist:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error(f"Event fetch error: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            # Authenticate and get user credentials
            user_credentials = GoogleCredentials.objects.get(email=request.user.email)
            
            # Create Google Calendar service
            credentials = Credentials(
                None,
                refresh_token=user_credentials.refresh_token,
                token_uri='https://oauth2.googleapis.com/token',
                client_id=settings.GOOGLE_OAUTH_CLIENT_ID,
                client_secret=settings.GOOGLE_OAUTH_CLIENT_SECRET,
            )
            credentials.refresh(Request())
            
            service = build('calendar', 'v3', credentials=credentials)
            
            required_fields = ['summary', 'dateTime']
            for field in required_fields:
                if field not in request.data:
                    return Response({'error': f'Missing {field}'}, status=status.HTTP_400_BAD_REQUEST)
            
            event = {
                'summary': request.data['summary'],
                'location': request.data.get('location'),
                'start': {
                    'dateTime': request.data['dateTime'],
                    'timeZone': 'UTC'
                },
                'end': {
                    'dateTime': request.data['dateTime'],
                    'timeZone': 'UTC'
                }
            }
            
            created_event = service.events().insert(calendarId='primary', body=event).execute()
            
            return Response({
                'event': {
                    'summary': created_event['summary'],
                    'dateTime': created_event['start'].get('dateTime'),
                    'location': created_event.get('location')
                }
            }, status=status.HTTP_201_CREATED)
        
        except GoogleCredentials.DoesNotExist:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error(f"Event creation error: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

