from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
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


# send letter to admin when user add new review
# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         msg = EmailMultiAlternatives(
#             subject='У вас новое сообщение с форума гиков',
#             from_email='olga-olechka-5@yandex.ru',
#             to=[f'{instance.reply_post.post_author.email}', ]
#         )
#
#         html_content = render_to_string(
#             'reply_added_letter.html',
#             {'reply': instance})
#
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()