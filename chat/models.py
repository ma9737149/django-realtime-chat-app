from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
import hashlib
import os


def get_file_hash(file):
    hasher = hashlib.sha256()
    file.seek(0)
    for chunk in file.chunks():
        hasher.update(chunk)
    file.seek(0)
    return hasher.hexdigest()

class HashedImageField(models.ImageField):
    def generate_filename(self, instance, filename):
        file = instance.__dict__.get(self.attname)
        if file:
            file_hash = get_file_hash(file.file)
            ext = os.path.splitext(filename)[1].lower()
            new_filename = f"{file_hash}{ext}"
            return os.path.join(self.upload_to, new_filename)
        return super().generate_filename(instance, filename)

    def save_form_data(self, instance, data):
        super().save_form_data(instance, data)

class UserProfile(AbstractUser):
    profile = HashedImageField(upload_to='users/' , default = 'defaults/default-img.png')