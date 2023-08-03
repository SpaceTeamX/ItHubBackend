from knox.models import AuthToken
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class AnotherProfileAPIView(generics.RetrieveAPIView):
    serializer_class = AnotherProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        user_id = self.kwargs["user_id"]
        try:
            user = User.objects.get(id=user_id)
        except:
            raise ValidationError({"error": "User not found"})

        profile = Profile.objects.get(user=user)
        return profile


class MeProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MeProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        profile = Profile.objects.get(user=self.request.user)
        return profile

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super(MeProfileAPIView, self).update(request, *args, **kwargs)


class AccountAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super(AccountAPIView, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        serializer = DeleteUserSerializer(
            instance=self.get_object(),
            data=request.data,
            context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class PasswordResetAPIView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = self.request.user
        serializer = self.get_serializer(data=request.data, instance=user, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
