from rest_framework.pagination import PageNumberPagination


class MyBasePagination(PageNumberPagination):
    page_size = 6
