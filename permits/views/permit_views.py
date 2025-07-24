from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.shortcuts import get_object_or_404

from permits.models import Permit
from permits.serializers.permit_serializers import PermitSerializer
from permits.pagination import CustomPermitPagination
from permits.permissions import IsAdminUserRole, IsCitizenUserRole
from permits.utils.validators import (
  validate_approval_conditions,
  validate_revocation_conditions
)
from permits.utils.responses import success_response, error_response


class PermitListView(ListAPIView):
  queryset = Permit.objects.select_related('user')
  serializer_class = PermitSerializer
  permission_classes = [IsAuthenticated]
  pagination_class = CustomPermitPagination

  def get_queryset(self):
    status_param = self.request.query_params.get("status")
    valid_statuses = [choice[0] for choice in Permit.STATUS_CHOICES]

    if status_param:
      if status_param not in valid_statuses:
        raise ValidationError({"status": f"Invalid status '{status_param}'. Valid options are: {valid_statuses}"})
      return Permit.objects.filter(status=status_param)

    return Permit.objects.all()


class PermitCreateView(CreateAPIView):
  serializer_class = PermitSerializer
  permission_classes = [IsAuthenticated, IsCitizenUserRole]

  def get_serializer_context(self):
    context = super().get_serializer_context()
    context["validate_for"] = "permit_create"
    return context

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

  def create(self, request, *args, **kwargs):
    return success_response("Permit created successfully", super().create(request, *args, **kwargs).data, status.HTTP_201_CREATED)


class ApprovePermitView(APIView):
  permission_classes = [IsAuthenticated, IsAdminUserRole]

  def post(self, request, pk):
    permit = get_object_or_404(Permit, pk=pk)
    try:
      validate_approval_conditions(permit)
    except ValidationError as e:
      error_message = e.detail[0] if isinstance(e.detail, list) else e.detail
      return error_response(error_message)
    except Exception as e:
      return error_response(str(e))

    permit.status = 'approved'
    permit.save()
    return success_response("Permit approved successfully", PermitSerializer(permit).data)


class RevokePermitView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def post(self, request, pk):
      permit = get_object_or_404(Permit, pk=pk)
      reason = request.data.get('revocation_reason')

      try:
        validate_revocation_conditions(permit,reason)
      except ValidationError as e:
        error_message = e.detail[0] if isinstance(e.detail, list) else e.detail
        return error_response(error_message)
      except Exception as e:
        return error_response(str(e))

      permit.status = 'revoked'
      permit.revocation_reason = reason
      permit.save()
      return success_response("Permit revoked successfully", PermitSerializer(permit).data)
