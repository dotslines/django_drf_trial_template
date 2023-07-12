from rest_framework.renderers import (
    # BaseRenderer,
    JSONRenderer
)


class CustomJSONRenderer(JSONRenderer):
    """
    Custom json renderer class.
    """
    def render(self, data,
               accepted_media_type=None,
               renderer_context=None):
        """
        changing response format,
        'message' and 'errors' added
        """
        formated_data = {
            "message": "",
            "errors": [],
            "data": data,
            "status": "success"
        }
        return super().render(
            formated_data,
            accepted_media_type,
            renderer_context
        )


# class JPEGRenderer(BaseRenderer):
#     media_type = 'image/jpeg'
#     format = 'jpg'
#     charset = None
#     render_style = 'binary'

#     def render(self, data,
#                accepted_media_type=None,
#                renderer_context=None):
#         return data
