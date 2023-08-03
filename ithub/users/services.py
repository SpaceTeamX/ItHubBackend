from rest_framework.exceptions import ValidationError


def get_path_upload_user_avatar(instance, filename):
    return f"users/{instance.id}/avatar.{filename.split('.')[-1]}"


def validate_size_image(file):
    limit_size = 5

    if file.size > limit_size * 1024 * 1024:
        raise ValidationError(f'Max size file: {limit_size}MB')
