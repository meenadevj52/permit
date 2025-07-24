import pytest
from django.utils import timezone
from datetime import timedelta

from permits.models import Permit, User
from permits.tasks import expire_old_pending_permits


@pytest.mark.django_db
def test_expire_old_pending_permits():
  user = User.objects.create_user(username="citizen1", password="pass", role="citizen")

  expired_permit = Permit.objects.create(
    user=user,
    name="Old Permit",
    license_plate="OLD123",
    address="Old Street",
    status="pending",
  )
  expired_permit.created_at = timezone.now() - timedelta(minutes=10)
  expired_permit.save()

  recent_permit = Permit.objects.create(
    user=user,
    name="Recent Permit",
    license_plate="NEW123",
    address="New Street",
    status="pending"
  )

  approved_permit = Permit.objects.create(
    user=user,
    name="Approved Permit",
    license_plate="APPROVED123",
    address="Approved Street",
    status="approved"
  )

  expire_old_pending_permits()

  expired_permit.refresh_from_db()
  recent_permit.refresh_from_db()
  approved_permit.refresh_from_db()

  assert expired_permit.status == "expired"
  assert recent_permit.status == "pending"
  assert approved_permit.status == "approved"
