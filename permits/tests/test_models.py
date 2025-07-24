import pytest
from permits.models import User, Permit

@pytest.fixture
def citizen_user(db):
  return User.objects.create_user(
    username="testuser",
    email="test@example.com",
    password="testpass123",
    role="citizen"
  )

@pytest.mark.django_db
class TestPermitModel:

  def test_create_user_with_role(self, citizen_user):
    assert citizen_user.username == "testuser"
    assert citizen_user.email == "test@example.com"
    assert citizen_user.role == "citizen"
    assert citizen_user.check_password("testpass123")

  def test_create_permit(self, citizen_user):
    permit = Permit.objects.create(
      user=citizen_user,
      name="John Doe",
      license_plate="AB123CD",
      address="123 Main St"
    )

    assert permit.user == citizen_user
    assert permit.name == "John Doe"
    assert permit.license_plate == "AB123CD"
    assert permit.address == "123 Main St"
    assert permit.status == "pending"
    assert permit.created_at is not None
    assert permit.updated_at is not None

  def test_permit_status_update(self, citizen_user):
    permit = Permit.objects.create(
      user=citizen_user,
      name="Jane Doe",
      license_plate="CD456EF",
      address="456 Side St"
    )
    permit.status = "approved"
    permit.save()

    assert Permit.objects.get(id=permit.id).status == "approved"

  def test_revoke_permit(self, citizen_user):
    permit = Permit.objects.create(
      user=citizen_user,
      name="Adam Smith",
      license_plate="XY789GH",
      address="789 Elm St",
      status="revoked",
      revocation_reason="Fake documents"
    )

    assert permit.status == "revoked"
    assert permit.revocation_reason == "Fake documents"
