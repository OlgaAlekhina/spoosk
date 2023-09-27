from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='/avatars/Noted_avatar.png', upload_to='avatars')
    name = models.CharField(max_length=30, default='Username')
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    website = models.CharField(max_length=50)


    def __str__(self):
        return self.name
