from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from .models import Category, Question


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class QuestionSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    categories = CategorySerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'
