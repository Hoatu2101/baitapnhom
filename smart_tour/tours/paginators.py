from rest_framework import pagination

class ItemPaginator(pagination.PageNumberPagination):
    page_size = 5

class ServicePaginator(pagination.PageNumberPagination):
    page_size = 20


class ReviewPagination(pagination.PageNumberPagination):
    page_size = 10
