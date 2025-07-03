from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

class EncryptedImageField(models.ImageField):
    def save(self, name, content, save=True):
        image_data = content.read()  
        encrypted_data = cipher.encrypt(image_data) 
        
        encrypted_content = ContentFile(encrypted_data)
        
        super().save(name, encrypted_content, save)

class UserProfile(AbstractUser):
    profile = EncryptedImageField(upload_to='users/' , default = 'defaults/default-img.png')