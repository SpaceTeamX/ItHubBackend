from drf_writable_nested import WritableNestedModelSerializer
from knox.models import User
from users.models import User
from taggit.models import Tag
from rest_framework import serializers
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField

from .models import Category, Question, Comment


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ("name",)
        lookup_field = 'name'
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class QuestionSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()
    author = serializers.SlugRelatedField(slug_field="username",
                                          queryset=User.objects.all())


    class Meta:
        model = Question
        fields = '__all__'
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class CommentSerializer(serializers.ModelSerializer):

    username = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    text = serializers.SlugRelatedField(slug_field="slug", queryset=Question.objects.all())

    class Meta:
        model = Comment
        fields = ("id", "content", "username", "text", "created_date")
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }