from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPermitPagination(PageNumberPagination):
  page_size = 5
  page_size_query_param = 'page_size'
  max_page_size = 100

  def get_paginated_response(self, data):
    count = self.page.paginator.count
    status_param = self.request.query_params.get("status")

    if count == 0:
      message = "No record found."
      data = []
    else:
      message = f"List of {count} {status_param} permits retrieved successfully." if status_param else f"List of {count} permits retrieved successfully."

    return Response({
      "message": message,
      "count": count,
      "current": self.page.number,
      "next": self.get_next_link(),
      "previous": self.get_previous_link(),
      "results": data,
    })