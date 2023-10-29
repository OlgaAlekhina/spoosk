from django.db import models
from django.contrib.auth.models import User
from urllib.request import urlopen
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', blank=True)
    name = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)

    def __str__(self):
        return self.user.username

    def get_image_from_url(self, url):
        img_tmp = NamedTemporaryFile()
        with urlopen(url) as uo:
            assert uo.status == 200
            img_tmp.write(uo.read())
            img_tmp.flush()
        img = File(img_tmp)
        # img_name = f'{img_tmp.name}.jpg'
        self.avatar.save('test.jpg', img)
