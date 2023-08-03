# Generated by Django 4.2.3 on 2023-08-03 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vacancy', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacancy',
            name='image',
        ),
        migrations.AddField(
            model_name='imagevacancy',
            name='vacancy',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='vacancy.vacancy'),
            preserve_default=False,
        ),
    ]