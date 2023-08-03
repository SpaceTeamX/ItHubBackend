from rest_framework.exceptions import ValidationError


def get_path_images_vacancy(instance, filename):
    return f"vacancy/{instance.vacancy.id}/{filename}"


def validate_size_image_vacancy(file):
    limit_size = 15

    if file.size > limit_size * 1024 * 1024:
        raise ValidationError(f'Max size file: {limit_size}MB')
