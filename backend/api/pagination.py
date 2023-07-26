from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from recipes.consts import MAX_PAGE_SIZE, PAGE_SIZE


class CustomLimitPageNumberPagination(PageNumberPagination):
    """Custom paginator with limit and page query."""
    page_size = PAGE_SIZE
    page_query_param = 'limit'
    max_page_size = MAX_PAGE_SIZE
    ordering = 'pk'

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data
        })
