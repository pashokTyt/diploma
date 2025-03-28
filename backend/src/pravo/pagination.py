from rest_framework.pagination import PageNumberPagination

class PublishedNpaPagination(PageNumberPagination):
    page_size = 10  # записей на странице
    page_size_query_param = 'size'  # параметр страницы, в запросе отображается
    max_page_size = 150  # максимыльный размер страницы
    