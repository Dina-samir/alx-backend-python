# chats/pagination.py

from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 20  # default page size
    page_size_query_param = 'page_size'  # allow client to override
    max_page_size = 100
