from rest_framework import serializers
import re
from django.contrib.auth.models import User


# validator for password length
def validate_password_length(password):
    if len(password) < 8 or len(password) > 128:
        raise serializers.ValidationError("Пароль должен содержать от 8 до 128 символов")
    return password


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
    if re.search(email_pattern, email) and len(email) < 51:
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