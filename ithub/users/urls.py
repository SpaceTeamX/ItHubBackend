from django.urls import path, include

from .views import UserAPIView

urlpatterns = [
    path("list/", UserAPIView.as_view()),
    path("auth/", include("rest_framework.urls"))
]

