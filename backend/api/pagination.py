from django.conf import settings
from rest_framework.pagination import PageNumberPagination

PAGE_SIZE = settings.PAGE_SIZE


class Pagination(PageNumberPagination):
    page_size = PAGE_SIZE
    page_size_query_param = 'limit'
