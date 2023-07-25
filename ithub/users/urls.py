from django.urls import path
from knox.views import LogoutView, LogoutAllView

from .views import *

urlpatterns = {
    path('auth/login/', LoginAPIView.as_view()),
    path('auth/register/', RegistrationAPIView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('auth/logout-all/', LogoutAllView.as_view()),
    path('me/profile/', MeProfileAPIView.as_view()),
    path('<int:user_id>/profile/', AnotherProfileAPIView.as_view()),
    path("me/reset-password/", PasswordResetAPIView.as_view())
}

