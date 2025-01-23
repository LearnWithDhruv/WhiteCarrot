from django.urls import path
from .views import GoogleLoginView, CalendarEventsView

urlpatterns = [
    path('auth/login/', GoogleLoginView.as_view(), name='google-login'),
    path('calendar/events/', CalendarEventsView.as_view(), name='calendar-events'),
]
