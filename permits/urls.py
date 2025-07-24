from django.urls import path
from .views import (
  PermitCreateView, PermitListView,
  ApprovePermitView, RevokePermitView,
  RegisterView, CustomAuthToken,
)

urlpatterns = [
  path('permits/create/', PermitCreateView.as_view(), name='create-permit'),
  path('permits/list/', PermitListView.as_view(), name='list-permits'),
  path('permits/<int:pk>/approve/', ApprovePermitView.as_view(), name='approve-permit'),
  path('permits/<int:pk>/revoke/', RevokePermitView.as_view(), name='revoke-permit'),

  path('register/', RegisterView.as_view(), name='register'),
  path('login/', CustomAuthToken.as_view(), name='login'),
]