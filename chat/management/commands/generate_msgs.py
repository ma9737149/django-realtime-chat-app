import random
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from chat.models import Room, Message, UserProfile

class Command(BaseCommand):
    help = "Generate random messages (including replies) in a specific room by a user"

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the message author')
        parser.add_argument('room_id', type=int, help='ID of the room to add messages into')
        parser.add_argument('--messages', type=int, default=10, help='Number of messages to create')

    def handle(self, *args, **options):
        username = options['username']
        room_id = options['room_id']
        messages_count = options['messages']

        try:
            user = UserProfile.objects.get(username=username)
        except UserProfile.DoesNotExist:
            raise CommandError(f"User with username '{username}' does not exist.")

        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            raise CommandError(f"Room with id '{room_id}' does not exist.")

        created_messages = []

        for i in range(1, messages_count + 1):
            content = f"Sample message {i} in {room.room_name}"

            if created_messages and random.choice([True, False]):
                reply_to = random.choice(created_messages)
            else:
                reply_to = None

            msg = Message.objects.create(
                message_content=content,
                message_author=user,
                room=room,
                reply_to=reply_to,
                created_at=timezone.now()
            )
            created_messages.append(msg)

        self.stdout.write(self.style.SUCCESS(f"Added {messages_count} messages to room '{room.room_name}'"))
