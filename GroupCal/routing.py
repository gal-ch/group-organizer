# from django.conf.urls import url
# from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
# from channels.auth import AuthMiddlewareStack
# from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
#
# from main.consumers import EventConsumer
#
# application = ProtocolTypeRouter({
#     # Websocket chat handler
#     'websocket': AllowedHostsOriginValidator(
#         AuthMiddlewareStack(
#             URLRouter(
#                 [
#                     url(r"calendar/$", EventConsumer, name='chat')
#                 ]
#             )
#         ),
#     ),
# })
#
