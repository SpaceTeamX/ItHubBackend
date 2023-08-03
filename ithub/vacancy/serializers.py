from os import remove

from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from .models import Vacancy, Contact, ImageVacancy


class ContactSerializer(serializers.ModelSerializer):
    vacancy = serializers.HiddenField(required=False, default=serializers.empty)

    class Meta:
        model = Contact
        fields = "__all__"


class ImageVacancySerializer(serializers.ModelSerializer):
    vacancy = serializers.HiddenField(required=False, default=serializers.empty)

    class Meta:
        model = ImageVacancy
        fields = '__all__'

    def update(self, instance, validated_data):
        try:
            remove(instance.image.path)
        except Exception as ex:
            print(ex)

        return super().update(instance, validated_data)


class VacancySerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    contact = ContactSerializer(many=True, required=False)
    images = serializers.SerializerMethodField("get_images", read_only=True)
    contacts = serializers.SerializerMethodField("get_contacts")
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    def get_images(self, obj):
        print(obj)
        return ImageVacancySerializer(
            ImageVacancy.objects.filter(vacancy=obj),
            many=True
        ).data

    def get_contacts(self, obj):
        print(obj)
        return ContactSerializer(
            Contact.objects.filter(vacancy=obj),
            many=True
        ).data

    class Meta:
        model = Vacancy
        fields = "__all__"
