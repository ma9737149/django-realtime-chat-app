from django.db import models
from django.contrib.auth.models import AbstractUser
import os
import uuid
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


def uuid_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    new_filename = f"{uuid.uuid4()}{ext}"
    return os.path.join('users/', new_filename)



class UserProfile(AbstractUser):
    email = models.EmailField(unique=True , blank=False , null=False)
    profile = models.ImageField(upload_to=uuid_upload_to , default = 'defaults/default-img.png' , validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])])
    is_online = models.BooleanField(default=False)


    def clean(self):
        super().clean()
        if self.profile:
            max_size = 2 * 1024 * 1024 
            if self.profile.size > max_size:
                raise ValidationError("Image file too large ( > 2MB )")

class Room(models.Model):
    room_name = models.CharField(max_length=100)
    room_description = models.CharField(max_length=300)
    room_author = models.ForeignKey(UserProfile , on_delete=models.CASCADE , related_name="rooms")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['room_name' , 'room_author']


class Message(models.Model):
    message_content = models.CharField(max_length=4000)
    message_author = models.ForeignKey(UserProfile , on_delete=models.CASCADE , related_name = "messages")
    created_at = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")


