
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from forum.views import QuestionViewSet, TagDetailView, TagView, CommentView
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
    path("tags/", TagView.as_view()),
    path("tags/<slug:tag_slug>/", TagDetailView.as_view()),
    path("comments/", CommentView.as_view()),
    path("comments/<post_slug>/", CommentView.as_view()),
    path("ckeditor/", include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
