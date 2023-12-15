from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, SignupCode
from rest_framework.validators import UniqueValidator
from random import randint
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .validators import validate_password_symbols, validate_email, email_exists


# serializer for UserProfile model
class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('avatar', )


# serializer for SignupCode model
class CodeSerializer(serializers.ModelSerializer):
    code = serializers.IntegerField(max_value=9999)

    class Meta:
        model = SignupCode
        fields = ('code', )


# serializer for User model for login endpoint
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True, max_length=50, validators=[validate_email])
    password = serializers.CharField(required=True, min_length=8, max_length=128, validators=[validate_password_symbols])

    class Meta:
        model = User
        fields = ('email', 'password')


# serializer for User model for reset password request endpoint
class ResetpasswordSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=50, validators=[validate_email, email_exists])

    class Meta:
        model = User
        fields = ('email', )


# serializer for User model for change password endpoint
class ChangepasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=128, validators=[validate_password_symbols])

    class Meta:
        model = User
        fields = ('password', )


# serializer for User model for registration endpoint
class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=50, validators=[UniqueValidator(queryset=User.objects.all(), message='Пользователь с таким email адресом уже существует'), validate_email])
    first_name = serializers.CharField(required=True, max_length=20)
    password = serializers.CharField(write_only=True, min_length=8, max_length=128, validators=[validate_password_symbols])

    class Meta:
        model = User
        fields = ('id', 'first_name', 'email', 'password')

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        first_name = validated_data['first_name']
        user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name)
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
    avatar = serializers.ImageField(source='userprofile.avatar', required=True)
    # profile = ProfileSerializer(source='userprofile', required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'date_joined', 'avatar')