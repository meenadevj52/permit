from rest_framework.response import Response
from rest_framework import status


def success_response(message, data=None, status_code=status.HTTP_200_OK):
  return Response({
    "message": message,
    "data": data
  }, status=status_code)


def error_response(error_message, status_code=status.HTTP_400_BAD_REQUEST):
  return Response({
    "error": error_message
  }, status=status_code)
