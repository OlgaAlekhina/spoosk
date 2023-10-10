from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='/avatars/dog1.jpg', upload_to='avatars', blank=True)
    name = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)

    def __str__(self):
        return self.user.username
