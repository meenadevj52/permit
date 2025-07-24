from rest_framework.permissions import BasePermission

class IsAdminUserRole(BasePermission):
  def has_permission(self, request, view):
    return request.user.role == 'admin'

class IsCitizenUserRole(BasePermission):
  def has_permission(self, request, view):
    return request.user.role == 'citizen'