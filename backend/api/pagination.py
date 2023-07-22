from rest_framework.pagination import PageNumberPagination


class CustomLimitPageNumberPagination(PageNumberPagination):
    page_size = 6
    page_query_param = 'limit'
    max_page_size = 50
