 import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory

from permits.serializers.auth_serializers import RegisterSerializer, CustomAuthTokenSerializer
from permits.serializers.permit_serializers import PermitSerializer
from permits.models import Permit

User = get_user_model()


@pytest.mark.django_db
class TestRegisterSerializer:

  def test_valid_data(self):
    data = {
      'username': 'TestUser',
      'email': 'test@example.com',
      'password': 'Valid@123'
    }
    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid() is True
    user = serializer.save()
    assert user.username == 'TestUser'
    assert user.role == 'citizen'
    assert user.check_password('Valid@123') is True

  def test_invalid_password_no_special_char(self):
    data = {
      'username': 'User1',
      'email': 'user1@example.com',
      'password': 'Password123'
    }
    serializer = RegisterSerializer(data=data)
    with pytest.raises(ValidationError) as e:
        serializer.is_valid(raise_exception=True)
    assert "Password must contain at least one special character." in str(e.value)

  def test_invalid_password_too_long(self):
    data = {
      'username': 'User2',
      'email': 'user2@example.com',
      'password': 'VeryLongPassword@12345678'
    }
    serializer = RegisterSerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
class TestCustomAuthTokenSerializer:

  def test_valid_login(self):
    user = User.objects.create_user(username='testuser', email='test@example.com', password='Valid@123')
    request = APIRequestFactory().post('/api/auth/')
    serializer = CustomAuthTokenSerializer(data={'username': 'testuser', 'password': 'Valid@123'}, context={'request': request})
    assert serializer.is_valid()
    assert serializer.validated_data['user'] == user

  def test_wrong_username(self):
    serializer = CustomAuthTokenSerializer(data={'username': 'wronguser', 'password': 'anything'})
    with pytest.raises(ValidationError) as e:
        serializer.is_valid(raise_exception=True)
    assert "Username does not exist." in str(e.value)

  def test_wrong_password(self):
    User.objects.create_user(username='testuser', email='test@example.com', password='Valid@123')
    request = APIRequestFactory().post('/api/auth/')
    serializer = CustomAuthTokenSerializer(data={'username': 'testuser', 'password': 'Wrong@123'}, context={'request': request})
    with pytest.raises(ValidationError) as e:
      serializer.is_valid(raise_exception=True)
    assert "Incorrect password." in str(e.value)


  def test_invalid_missing_fields(self):
    user = User.objects.create_user(username='john', password='Test@123')
    request = APIRequestFactory().post('/api/permits/')
    request.user = user
    data = {}
    context = {'request': request, 'validate_for': 'permit_create'}
    serializer = PermitSerializer(data=data, context=context)
    assert serializer.is_valid() is False
    assert 'name' in serializer.errors
    assert 'license_plate' in serializer.errors
    assert 'address' in serializer.errors

