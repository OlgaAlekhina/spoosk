from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile


# create userprofile for new users
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        email = instance.email
        dog_spot = email.find('@')
        name = email[:dog_spot]
        UserProfile.objects.create(user=instance, name=name)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()


