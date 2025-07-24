import pytest
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from permits.permissions import IsAdminUserRole, IsCitizenUserRole
from permits.models import User


@pytest.mark.django_db
class TestCustomPermissions:

  def setup_method(self):
    self.factory = APIRequestFactory()

  def test_is_admin_user_role_permission(self):
    user = User.objects.create_user(username="admin1", password="pass", role="admin")
    request = self.factory.get("/some-url/")
    request.user = user

    permission = IsAdminUserRole()
    assert permission.has_permission(request, None) is True

  def test_is_admin_user_role_permission_denied(self):
    user = User.objects.create_user(username="citizen1", password="pass", role="citizen")
    request = self.factory.get("/some-url/")
    request.user = user

    permission = IsAdminUserRole()
    assert permission.has_permission(request, None) is False

  def test_is_citizen_user_role_permission(self):
    user = User.objects.create_user(username="citizen1", password="pass", role="citizen")
    request = self.factory.get("/some-url/")
    request.user = user

    permission = IsCitizenUserRole()
    assert permission.has_permission(request, None) is True

  def test_is_citizen_user_role_permission_denied(self):
    user = User.objects.create_user(username="admin1", password="pass", role="admin")
    request = self.factory.get("/some-url/")
    request.user = user

    permission = IsCitizenUserRole()
    assert permission.has_permission(request, None) is False
