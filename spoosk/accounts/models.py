from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars", blank=True)
    name = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username

    def get_image_from_url(self, url):
        r = requests.get(url)
        img_temp = NamedTemporaryFile()
        img_temp.write(r.content)
        img_temp.flush()
        url_split = url.split('/')
        name = url_split[-1]
        img_name = f'{name}.jpg'
        self.avatar.save(img_name, File(img_temp), save=True)
        return self.avatar


class SignupCode(models.Model):
    code = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code_time = models.DateTimeField(auto_now_add=True)