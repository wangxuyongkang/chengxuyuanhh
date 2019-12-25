from rest_framework.pagination import PageNumberPagination
class MyPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    page_size_query_param = 'pagesize'
    max_page_size = 10