from rest_framework.pagination import PageNumberPagination



class StandardPagination(PageNumberPagination):
    page_size = 10      # Determine the default page size (the no. of items returned per page) when
    # no page size is provided in the request
    page_size_query_param = 'page_size'     # Defines the name for the query parameter to use for the page size
    max_page_size = 50      # Indicates the maximum requested page size allowed