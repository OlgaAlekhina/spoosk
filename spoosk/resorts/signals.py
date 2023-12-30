from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import SkiReview


# send letter to admin when user add new review
@receiver(post_save, sender=SkiReview)
def create_profile(sender, instance, created, **kwargs):
    if created:
        msg = EmailMultiAlternatives(
            subject='Новый отзыв на модерации в приложении Spoosk',
            from_email='spoosk.info@gmail.com',
            to=['olga-alekhina@rambler.ru', ]
        )

        html_content = render_to_string(
            'add_review_letter.html',
            {'id': instance.id})

        msg.attach_alternative(html_content, "text/html")
        msg.send()