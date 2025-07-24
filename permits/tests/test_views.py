import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from permits.models import Permit

User = get_user_model()


# Fixtures


@pytest.fixture
def api_client():
  return APIClient()

@pytest.fixture
def citizen_user(db):
  return User.objects.create_user(username="citizen", email="citizen@example.com", password="citizen123", role="citizen")

@pytest.fixture
def admin_user(db):
  return User.objects.create_user(username="admin", email="admin@example.com", password="admin123", role="admin")

@pytest.fixture
def permit(db, citizen_user):
  return Permit.objects.create(user=citizen_user, license_plate="XY123AB", address="123 Street", status="pending")

@pytest.fixture
def approved_permit(db, citizen_user):
  return Permit.objects.create(user=citizen_user, license_plate="XY123AB", address="123 Street", status="approved")

@pytest.fixture
def revoked_permit(db, citizen_user):
  return Permit.objects.create(user=citizen_user, license_plate="XY123AB", address="123 Street", status="revoked")


# Auth Tests


@pytest.mark.django_db
class TestAuth:

  def test_register_user_success(self, api_client):
    url = reverse("register")
    payload = {
      "username": "newuser",
      "email": "newuser@example.com",
      "password": "Pass@1234",
      "role": "citizen"
    }
    response = api_client.post(url, payload)
    assert response.status_code == 201
    assert response.data["message"] == "User registered successfully"

  def test_login_success(self, api_client):
    User.objects.create_user(username="testuser", password="pass1234", email="test@example.com", role="citizen")
    url = reverse("login")
    payload = {"username": "testuser", "password": "pass1234"}
    response = api_client.post(url, payload)
    assert response.status_code == 200
    assert "token" in response.data["data"]

  def test_login_fail(self, api_client):
    url = reverse("login")
    response = api_client.post(url, {"username": "x", "password": "y"})
    assert response.status_code == 400


# Permit Creation


@pytest.mark.django_db
class TestPermitCreation:

  def test_permit_create_success(self, api_client, citizen_user):
    api_client.force_authenticate(user=citizen_user)
    url = reverse("create-permit")
    data = {
      "name": "citizen",
      "license_plate": "AB12CD1234",
      "address": "Some address"
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert response.data["message"] == "Permit created successfully"

  def test_permit_create_forbidden_for_admin(self, api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse("create-permit")
    data = {
      "vehicle_number": "AB12CD1234",
      "address": "Admin address"
    }
    response = api_client.post(url, data)
    assert response.status_code == 403


# Permit Listing


@pytest.mark.django_db
class TestPermitListing:

  def test_list_permits_success(self, api_client, citizen_user, permit):
    api_client.force_authenticate(user=citizen_user)
    url = reverse("list-permits")
    response = api_client.get(url)
    assert response.status_code == 200

  def test_list_permits_with_status_filter(self, api_client, citizen_user, permit):
    api_client.force_authenticate(user=citizen_user)
    url = reverse("list-permits") + "?status=pending"
    response = api_client.get(url)
    assert response.status_code == 200
    assert all(p["status"] == "pending" for p in response.data["results"])


# Permit Approval


@pytest.mark.django_db
class TestPermitApproval:

  def test_approve_permit_success(self, api_client, admin_user, permit):
    api_client.force_authenticate(user=admin_user)
    url = reverse("approve-permit", args=[permit.id])
    response = api_client.post(url)
    assert response.status_code == 200
    assert response.data["message"] == "Permit approved successfully"

  def test_approve_permit_forbidden(self, api_client, citizen_user, permit):
    api_client.force_authenticate(user=citizen_user)
    url = reverse("approve-permit", args=[permit.id])
    response = api_client.post(url)
    assert response.status_code == 403


# Permit Revocation


@pytest.mark.django_db
class TestPermitRevocation:

  def test_revoke_permit_success(self, api_client, admin_user, approved_permit):
    api_client.force_authenticate(user=admin_user)
    url = reverse("revoke-permit", args=[approved_permit.id])
    data = {"revocation_reason": "Expired"}
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert response.data["message"] == "Permit revoked successfully"

  def test_revoke_without_reason(self, api_client, admin_user, revoked_permit):
    api_client.force_authenticate(user=admin_user)
    url = reverse("revoke-permit", args=[revoked_permit.id])
    response = api_client.post(url, {})
    assert response.status_code in [400, 422]
