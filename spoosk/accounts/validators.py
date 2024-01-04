from rest_framework import serializers
import re
from django.contrib.auth.models import User


# validator for password symbols
def validate_password_symbols(password):
    password_pattern = '^[a-zA-Z0-9!#.$%&+=?^_`{|}~-]{2,}$'
    if re.search(password_pattern, password):
        return password
    else:
        raise serializers.ValidationError("Пароль содержит недопустимые символы")


# validator for email format
def validate_email(email):
    email_pattern = '^([a-zA-Z0-9!#.$%&+=?^_`{|}~-]+@[a-zA-Z0-9.-]+[a-zA-Z0-9]+\.[a-zA-Z]{2,})$'
    if re.search(email_pattern, email):
        return email
    else:
        raise serializers.ValidationError("Некорректно введен адрес электронной почты")


# validate if email exists in DB
def email_exists(email):
    user = User.objects.filter(email=email, is_active=True).first()
    if user:
        return email
    else:
        raise serializers.ValidationError("Пользователь с таким email адресом не зарегистрирован в приложении")


# on registration raise error if email exists and has been activated or delete account if email hasn't been activated
def check_status(email):
    user_inactive = User.objects.filter(email=email, is_active=False).first()
    if user_inactive:
        user_inactive.delete()
    user_active = User.objects.filter(email=email, is_active=True).first()
    if user_active:
        raise serializers.ValidationError("Пользователь с таким email адресом уже зарегистрирован в приложении")
    else:
        return email