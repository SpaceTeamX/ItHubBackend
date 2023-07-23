from django.urls import path

from .views import UserAPIView

urlpatterns = [
    path("list/", UserAPIView.as_view())
]
