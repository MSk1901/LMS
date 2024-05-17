from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):
    """Класс с настройками пагинации"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
