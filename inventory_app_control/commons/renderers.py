# from djangorestframework_camel_case.render import CamelCaseJSONRenderer
#
#
# class CustomJSONRenderer(CamelCaseJSONRenderer):
#     def render(self, data, accepted_media_type=None, renderer_context=None):
#         response_data = {}
#         errors = None
#
#         if 'error' in data:
#             errors = data['error']
#
#         if errors and len(errors) == 0:
#             errors = None
#
#         response_data['errors'] = errors
#
#         if errors is None:
#             response_data['data'] = data
#         else:
#             response_data['data'] = None
#
#         # getattr(renderer_context.get('view').get_serializer().Meta, 'resource_name', 'objects')
#         # call super to render the response
#         response = super(CustomJSONRenderer, self).render(response_data, accepted_media_type, renderer_context)
#         return response
