from django.db import models
from django.contrib.auth.models import AbstractUser
import os
import uuid

def uuid_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    new_filename = f"{uuid.uuid4()}{ext}"
    return os.path.join('users/', new_filename)



class UserProfile(AbstractUser):
    email = models.EmailField(unique=True , blank=False , null=False)
    profile = models.ImageField(upload_to=uuid_upload_to , default = 'defaults/default-img.png')