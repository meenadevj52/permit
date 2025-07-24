from rest_framework.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


def validate_approval_conditions(permit):
  if permit.status == 'approved':
    raise ValidationError("This permit has already been approved.")
  if permit.status != 'pending':
    raise ValidationError("Only pending permits can be approved.")
  if permit.created_at < timezone.now() - timedelta(minutes=5):
    raise ValidationError("Permits can only be approved within 5 minutes of creation.")


def validate_revocation_conditions(permit, reason):
  if permit.status == 'revoked':
    raise ValidationError("Permit is already revoked.")
  if permit.status != 'approved':
    raise ValidationError("Only approved permits can be revoked.")
  if not reason:
    raise ValidationError("Revocation reason is required.")
