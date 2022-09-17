from django.urls import re_path

from DdosTool import consumers

websocket_urlpatterns = [
    re_path('ws/datas/', consumers.Consumer.as_asgi()),
]
