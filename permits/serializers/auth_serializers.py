from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
import re

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)

  class Meta:
    model = User
    fields = ['id', 'username', 'email', 'password']

  def validate_password(self, value):
    
    if len(value) > 12:
      raise serializers.ValidationError("Password must not exceed 12 characters.")

    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
      raise serializers.ValidationError("Password must contain at least one special character.")

    
    if not re.search(r'[A-Z]', value):
      raise serializers.ValidationError("Password must contain at least one uppercase letter.")

    
    if not re.search(r'[a-z]', value):
      raise serializers.ValidationError("Password must contain at least one lowercase letter.")
      
    return value

  def create(self, validated_data):
    user = User(
      username=validated_data['username'],
      email=validated_data['email'],
      role='citizen',
    )
    user.set_password(validated_data['password'])
    user.save()
    return user




class CustomAuthTokenSerializer(serializers.Serializer):
  username = serializers.CharField(label="Username")
  password = serializers.CharField(label="Password", style={'input_type': 'password'})

  def validate(self, attrs):
    username = attrs.get('username')
    password = attrs.get('password')

    try:
      user = User.objects.get(username=username)
    except User.DoesNotExist:
      raise serializers.ValidationError({"username": "Username does not exist."})

    user = authenticate(request=self.context.get('request'), username=username, password=password)

    if not user:
      raise serializers.ValidationError({"password": "Incorrect password."})

    attrs['user'] = user
    return attrs
