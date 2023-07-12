from rest_framework.parsers import BaseParser


class CustomParser(BaseParser):
    """ Custom parser template """
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        return super().parse(stream, media_type, parser_context)
