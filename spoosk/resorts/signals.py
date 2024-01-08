from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import SkiReview
from django.conf import settings


# send letter to admin when user add new review
@receiver(post_save, sender=SkiReview)
def create_review(sender, instance, created, **kwargs):
    if created:
        msg = EmailMultiAlternatives(
            subject='Новый отзыв на модерации в приложении Spoosk',
            from_email='spoosk.info@gmail.com',
            to=['olga-alekhina@rambler.ru', ]
        )
        if settings.DEBUG:
            domain = 'http://127.0.0.1:8000'
        else:
            domain = 'https://spoosk.pnpl.tech'
        html_content = render_to_string(
            'accounts/add_review_letter.html',
            {'id': instance.id,
             'domain': domain})

        msg.attach_alternative(html_content, "text/html")
        msg.send()
