from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth import login
import random
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import user_token
import json
from .models import UserProfile


# обработка запроса на регистрацию
def signup_endpoint(request):
    if request.method == 'POST':
        username = f'{random.randrange(10000000000)}'
        usermail = request.POST.get('usermail')
        password = request.POST.get('password')
        if User.objects.filter(email=usermail).exists():
            return JsonResponse({"error": "User with such email address already exists!"}, status=403)
        else:
            user = User.objects.create_user(username=username, password=password, email=usermail)
            user.is_active = False
            user.save()
            msg = EmailMultiAlternatives(
                subject='Регистрация на сайте Spoosk',
                from_email='spoosk.info@gmail.com',
                to=[user.email, ]
            )
            html_content = render_to_string(
                'signup_confirmation.html',
                {'domain': request.get_host(),
                 'user': user,
                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                 'token': user_token.make_token(user),
                 'protocol': 'https' if request.is_secure() else 'http'}
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return JsonResponse({"success": "Check your email to finish registration!"}, status=200)
    else:
        raise Http404


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
        return redirect('resorts')
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
    else:
        raise Http404


# запрос на смену пароля
def reset_request(request):
    if request.method == 'POST':
        usermail = request.POST.get('user_mail')
        user = User.objects.filter(email=usermail).first()
        if user:
            msg = EmailMultiAlternatives(
                subject='Восстановление пароля на сайте Spoosk',
                from_email='spoosk.info@gmail.com',
                to=[user.email, ]
            )
            html_content = render_to_string(
                'reset_confirmation.html',
                {'domain': request.get_host(),
                 'user': user,
                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                 'token': user_token.make_token(user),
                 'protocol': 'https' if request.is_secure() else 'http'}
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return JsonResponse({"success": "Check your email for password reset confirmation!"}, status=200)
        else:
            return JsonResponse({"error": "There is no user with such email address!"}, status=403)
    else:
        raise Http404


# изменение пароля пользователя после подтверждения по mail
def reset_confirmation(request):
    uidb64 = request.GET.get('uidb64')
    token = request.GET.get('token')
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and user_token.check_token(user, token):
        response_data = {}
        response_data['result'] = 'Its a success!'
        response_data['user'] = user.username
        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json'
        )
    else:
        return render(request, 'link_expired.html', {})


# устанавливает новый пароль для пользователя
def reset_endpoint(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()
        user.set_password(password1)
        user.save()
        return JsonResponse({"success": "Changed password successfully!"}, status=200)
    else:
        raise Http404


# страница редактирования данных пользователя
def userprofile_page(request):
    return render(request, 'accounts/editing_account.html', {})


# временная функция для создания UserProfile для ранее созданных пользователей (удалить вместе с url после однократного использования на проде)
def add_missing_profiles(request):
    users = User.objects.all()
    for user in users:
        created = UserProfile.objects.get_or_create(user=user)
        print(user.username, ' : ', created)
    print("all done")
    return HttpResponse("It's done.")
