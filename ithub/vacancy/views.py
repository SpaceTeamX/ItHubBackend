from shutil import rmtree

from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from ithub.settings import MEDIA_ROOT
from .serializers import *
from .models import Vacancy


# Create your views here.
class VacancyViewSet(viewsets.ModelViewSet):
    serializer_class = VacancySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
            return Vacancy.objects.get(pk=pk)
        except:
            raise ValidationError("Vacancy not found")

    def get_queryset(self):
        return Vacancy.objects.all()[:10]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user == instance.user:
            return super().destroy(request, *args, **kwargs)

        return Response("Permission denied", status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        try:
            rmtree(MEDIA_ROOT / "vacancy" / str(instance.id))
        except Exception as ex:
            print(ex)

        instance.delete()


class ImagesVacancyViewSet(viewsets.ModelViewSet):
    serializer_class = ImageVacancySerializer

    def get_queryset(self):
        return ImageVacancy.objects.filter(vacancy=self.kwargs.get("vacancy_id"))

    def perform_create(self, serializer):
        try:
            vacancy = Vacancy.objects.get(pk=self.kwargs.get("vacancy_id"))
        except:
            raise ValidationError("Vacancy not found")

        if vacancy.user != self.request.user:
            raise ValidationError("Permissions denied")

        serializer.save(vacancy=vacancy)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user == instance.vacancy.user:
            return super().destroy(request, *args, **kwargs)

        return Response("Permission denied", status=status.HTTP_400_BAD_REQUEST)
