import json
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']    # retrieving the course_id from the scope
        self.room_group_name = f'chat_{self.id}'

        # join the group by adding channel to the group.
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        # accept connection
        await self.accept()

    async def disconnect(self, close_code):
        # leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # receive message from WebSocket -- i.e., from the browser (client)
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        # send message to WebSocket
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message', # This is a special key that corresponds to the name of the method that
                # should be invoked on consumers that receive the event.
                'message': message,     # The actual message you are sending.
                'user': self.user.username,
                'datetime': now.isoformat(),
            }
        )

    async def chat_message(self, event):
        # send message to WebSocket
        await self.send(text_data=json.dumps(event))  # sends the WHOLE dict from self.room_group_name
