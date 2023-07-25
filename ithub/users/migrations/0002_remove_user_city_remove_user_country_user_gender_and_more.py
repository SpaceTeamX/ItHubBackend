# Generated by Django 4.2.3 on 2023-07-25 17:58

import users.services
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='city',
        ),
        migrations.RemoveField(
            model_name='user',
            name='country',
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('he', 'Man'), ('she', 'Woman'), ('none', 'Anonymous')], default='none', max_length=4),
        ),
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='default/avatar.png', upload_to=users.services.get_path_upload_user_avatar, validators=[users.services.validate_size_image]),
        ),
    ]
