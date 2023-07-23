from rest_framework.pagination import PageNumberPagination

from recipes.consts import MAX_PAGE_SIZE, PAGE_SIZE


class CustomLimitPageNumberPagination(PageNumberPagination):
    """Custom paginator with limit and page query."""
    page_size = PAGE_SIZE
    page_query_param = 'limit'
    max_page_size = MAX_PAGE_SIZE
