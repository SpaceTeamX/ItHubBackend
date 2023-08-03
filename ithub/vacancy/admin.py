from django.contrib import admin

from vacancy.models import Vacancy, ImageVacancy, Contact

# Register your models here.
admin.site.register(Vacancy)
admin.site.register(ImageVacancy)
admin.site.register(Contact)
