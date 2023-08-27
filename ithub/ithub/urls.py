
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from forum.views import QuestionViewSet
from rest_framework import routers

from ithub import settings
from vacancy.views import*

router = routers.SimpleRouter()
router.register("vacancy", VacancyViewSet, "vacancy")
router.register("questions", QuestionViewSet, "questions")
router.register(r'vacancy/(?P<vacancy_id>\d+)/images', ImagesVacancyViewSet, basename="images")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
