from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
import json
from django.contrib.auth import login
import random
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import user_token


def signup(request):
    return render(request, 'signup.html', {})


# обработка запроса на регистрацию
def signup_endpoint(request):
    if request.method == 'POST':
        username = f'{random.randrange(10000000000)}'
        usermail = request.POST.get('usermail')
        password = request.POST.get('password')
        if User.objects.filter(email=usermail).exists():
            return JsonResponse({"error": "User with such email address already exists!"}, status=403)
        else:
            user = User(username=username, password=password, email=usermail)
            user.is_active = False
            user.save()
            msg = EmailMultiAlternatives(
                subject='Регистрация на сайте Spoosk',
                from_email='olga-olechka-5@yandex.ru',
                to=[user.email, ]
            )
            html_content = render_to_string(
                'signup_confirmation.html',
                {'domain': get_current_site(request).domain,
                 'user': user,
                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                 'token': user_token.make_token(user),
                 'protocol': 'https' if request.is_secure() else 'http'}
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return JsonResponse({"success": "Check your email to finish registration!"}, status=200)
    else:
        return render(request, 'test.html', {})


# подтверждение регистрации по email
def signup_confirmation(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and user_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'test.html', {})
    else:
        return render(request, 'link_expired.html', {})


# аутентификация пользователя по мейлу
def authenticate_user(email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user
    return None


# обработка запроса на авторизацию
def login_endpoint(request):
    if request.method == 'POST':
        user_mail = request.POST.get('user_mail')
        login_password = request.POST.get('login_password')
        user = authenticate_user(user_mail, login_password)
        if user is not None:
            login(request, user)
            return JsonResponse({"success": "The user was log in!"}, status=200)
        else:
            return JsonResponse({"error": "There is no user with such credentials!"}, status=403)

