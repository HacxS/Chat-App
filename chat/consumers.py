from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

import json
from django.conf import settings
import time

class ChatConsumer(WebsocketConsumer):
    
    def connect(self):
        if self.scope["user"].is_anonymous:
            self.accept()
            self.send(json.dumps({
                "status": "error",
                'message': f"Please authenticate by passing token in GET method"
                }))
            time.sleep(10)
            self.close()
        else:
            self.group_name = str(self.scope["user"].pk)
            async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
            self.accept()
            self.send(json.dumps({
                    "status": "success",
                    'message': f"Hey {self.scope['user'].username}, Welcome To Chat"
                }))

    def disconnect(self, close_code):
        self.close()

    def send_message(self, event):
        self.send(text_data=json.dumps({"status": "success","command": "new_message","type": event["message_type"], "data": event["text"]}))

    def delete_message(self,event):
        self.send(text_data=json.dumps({"status": "success","command": "deleted_message","type": event["message_type"], "deleted_id": event["text"]}))
