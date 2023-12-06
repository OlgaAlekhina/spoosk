from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, SignupCode
from rest_framework.validators import UniqueValidator
from random import randint
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# serializer for UserProfile model
class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('name', 'country', 'city', 'avatar')


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')


# serializer for User model for registration endpoint
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all(), message='Пользователь с таким email адресом уже существует')])

    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        user = User.objects.create_user(username=email, email=email, password=password)
        user.is_active = False
        user.save()
        code = SignupCode.objects.create(code=randint(1000, 9999), user=user)
        msg = EmailMultiAlternatives(
            subject='Регистрация в приложении Spoosk',
            from_email='spoosk.info@gmail.com',
            to=[user.email, ]
        )
        html_content = render_to_string(
            'accounts/signup_code.html',
            {'code': code.code}
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return user


# serializer for User model with profile options
class UserprofileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(source='userprofile', help_text="extra data on user", required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'date_joined', 'profile')