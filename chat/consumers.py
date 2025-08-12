from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
import datetime

class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("rooms", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("rooms", self.channel_name)

    async def receive(self, text_data):
        pass

    async def room_created(self, event):
        room = event["room"]
        await self.send(text_data=json.dumps({
            "type": "room.created",
            "room": room,
        }))


    async def room_updated(self, event):
        room = event["room"]
        await self.send(text_data=json.dumps({
            "type": "room.updated",
            "room": room,
        }))

    async def room_deleted(self, event):
        room = event["room"]
        await self.send(text_data=json.dumps({
            "type": "room.deleted",
            "room": room,
        }))



active_users = {}

class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_user_info(self, user):
        return {
            "id": str(user.id),
            "username": user.username,
            "avatar": user.profile.url,
            "joined_at": datetime.datetime.now().isoformat()
        }

    async def connect(self):
        user = self.scope.get("user")
        if not user or user.is_anonymous:
            await self.close(code=4001)
            return

        try:
            self.room_id = str(self.scope["url_route"]["kwargs"]["room_id"])
            self.room_group_name = f"chat_{self.room_id}"
            self.user = user
            
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            
            self.user_info = await self.get_user_info(self.user)
            
            if self.room_id not in active_users:
                active_users[self.room_id] = []
            
            user_exists = any(u["id"] == self.user_info["id"] for u in active_users[self.room_id])
            
            if not user_exists:
                active_users[self.room_id].append(self.user_info)
            
            await self.accept()
            
            await self.send_initial_data()
            
            await self.notify_user_activity("user_joined")
            
        except Exception as e:
            print(f"Connection error: {str(e)}")
            await self.close(code=4002)

    async def disconnect(self, close_code):
        try:
            if hasattr(self, 'room_id') and hasattr(self, 'user_info'):
                active_users[self.room_id] = [
                    u for u in active_users[self.room_id]
                    if u["id"] != self.user_info["id"]
                ]
                
                await self.notify_user_activity("user_left")
            
            if hasattr(self, 'room_group_name'):
                await self.channel_layer.group_discard(
                    self.room_group_name,
                    self.channel_name
                )
                
        except Exception as e:
            print(f"Disconnection error: {str(e)}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)

            
        except json.JSONDecodeError:
            await self.send_error("Invalid JSON format")
        except Exception as e:
            print(f"Message handling error: {str(e)}")

    async def send_initial_data(self):
        await self.send(text_data=json.dumps({
            "type": "initial_data",
            "active_users": active_users.get(self.room_id, []),
            "message": f"Welcome to room {self.room_id}!"
        }))

    async def notify_user_activity(self, event_type):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_activity",
                "event": event_type,
                "user": self.user_info,
                "message": f"{self.user_info['username']} has {'joined' if event_type == 'user_joined' else 'left'} the room",
                "timestamp": datetime.datetime.now().isoformat(),
                "active_users": active_users.get(self.room_id, [])
            }
        )

    async def send_error(self, message):
        await self.send(text_data=json.dumps({
            "type": "error",
            "message": message
        }))

    async def user_activity(self, event):
        if hasattr(self, 'user_info') and event["user"]["id"] == self.user_info["id"]:
            return
            
        await self.send(text_data=json.dumps({
            "type": event["event"],
            "user": event["user"],
            "message": event["message"],
            "timestamp": event["timestamp"],
            "active_users": event["active_users"]
        }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))