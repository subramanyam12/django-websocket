import json

from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        
        self.room_group_name = f"pad_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

   
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        
      
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "drawpad.copoints", "message": message,'sender_channel_name': self.channel_name,}
        )

  
    async def drawpad_copoints(self, event):
        message = event["message"]


        sender_channel_name = event['sender_channel_name']
       
        if self.channel_name != sender_channel_name:
            await self.send(text_data=json.dumps({"message": message}))
            

