import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class Consumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None

    def connect(self):
        self.room_group_name = 'Datas'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from room group
    def sendData(self, event):
        data = event['data']
        # Send message to WebSocket
        self.send(text_data=json.dumps({'data': data}))

    """
    def receive(self, data):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'sendData',
                'data': data
            }
        )
    """
