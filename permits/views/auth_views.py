from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from permits.serializers.auth_serializers import RegisterSerializer, CustomAuthTokenSerializer
from permits.utils.responses import success_response
from permits.utils.auth import get_user_token

User = get_user_model()


class RegisterView(generics.CreateAPIView):
  serializer_class = RegisterSerializer
  permission_classes = [AllowAny]

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    return success_response("User registered successfully", {
      "id": user.id,
      "username": user.username,
      "email": user.email,
      "role": user.role,
    }, status.HTTP_201_CREATED)


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
      serializer = self.serializer_class(data=request.data, context={'request': request})
      serializer.is_valid(raise_exception=True)
      user = serializer.validated_data['user']
      token = get_user_token(user)

      return success_response(f"{user.username} logged in successfully", {
        "token": token.key
      })
