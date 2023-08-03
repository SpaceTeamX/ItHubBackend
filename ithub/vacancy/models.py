from django.db import models

from vacancy.services import validate_size_image_vacancy, get_path_images_vacancy


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    vacancy = models.ForeignKey("Vacancy", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ImageVacancy(models.Model):
    vacancy = models.ForeignKey("Vacancy", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_path_images_vacancy,
                              validators=[validate_size_image_vacancy])

    def __str__(self):
        return self.image.name


class Vacancy(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=3000)
    profit = models.CharField(max_length=50, blank=True, default="Не указано")

    def __str__(self):
        return self.title


