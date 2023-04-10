from django.core.exceptions import MiddlewareNotUsed


class MiddlewareTemplate:
    def __init__(self, get_response) -> None:
        self._get_response = get_response
        # raise MiddlewareNotUsed()
    
    def __call__(self, request, *args, **kwds):
        response = self._get_response(request)
        return response
    
    def process_exception(self):
        pass