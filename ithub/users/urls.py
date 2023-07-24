from django.urls import path, include, re_path
from knox.views import LogoutView, LogoutAllView

from .views import LoginAPIView, RegistrationAPIView

urlpatterns = [
    path('auth/login/', LoginAPIView.as_view()),
    path('auth/register/', RegistrationAPIView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('auth/logout-all/', LogoutAllView.as_view()),
]

