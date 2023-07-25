from knox.models import AuthToken
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import *


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": MeUserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": MeUserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class AnotherProfileAPIView(generics.GenericAPIView):
    serializer_class = AnotherUserSerializer

    def get(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
        except:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(AnotherUserSerializer(user, context=self.get_serializer_context()).data)


class MeProfileAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = MeUserSerializer

    def get(self, request, *args, **kwargs):
        return Response(MeUserSerializer(self.request.user, context=self.get_serializer_context()).data)

    def put(self, request, *args, **kwargs):
        user = self.request.user

        serializer = MeUserSerializer(user, data=request.data, partial=True, context=self.get_serializer_context())

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        serializer = DeleteUserSerializer(instance=self.request.user, data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class PasswordResetAPIView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        user = self.request.user
        serializer = PasswordResetSerializer(data=request.data, instance=user, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
