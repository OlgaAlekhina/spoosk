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
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
import requests
from resorts.models import SkiReview


# обработка запроса на регистрацию
def signup_endpoint(request):
    if request.method == 'POST':
        username = request.POST.get('usermail')
        usermail = request.POST.get('usermail')
        password = request.POST.get('password')
        if User.objects.filter(email=usermail).exists():
            return JsonResponse({"error": "Пользователь с таким email адресом уже существует"}, status=403)
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
        return redirect('userprofile_page')
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
            return JsonResponse({"error": "Неправильно введены учетные данные"}, status=403)
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
            return JsonResponse({"error": "Пользователя с таким email адресом не существует"}, status=403)
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


# вход и/или регистрация пользователя через учетную запись Google
def google_login(request):
    redirect_uri = "%s://%s%s" % (
        request.scheme, request.get_host(), reverse('google_login')
    )
    print(redirect_uri)
    if ('code' in request.GET):
        params = {
            'grant_type': 'authorization_code',
            'code': request.GET.get('code'),
            'redirect_uri': redirect_uri,
            'client_id': settings.GP_CLIENT_ID,
            'client_secret': settings.GP_CLIENT_SECRET
        }
        url = 'https://accounts.google.com/o/oauth2/token'
        response = requests.post(url, data=params)
        url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        access_token = response.json().get('access_token')
        response = requests.get(url, params={'access_token': access_token})
        user_data = response.json()
        email = user_data.get('email')
        if email:
            user, _ = User.objects.get_or_create(email=email, username=email)
            data = {
                'first_name': user_data.get('name', '').split()[0],
                'last_name': user_data.get('family_name', ''),
                'is_active': True
            }
            user.__dict__.update(data)
            user.save()
            login(request, user)
            picture = user_data.get('picture')
            profile = UserProfile.objects.get(user=user)
            if not profile.avatar:
                profile.avatar = profile.get_image_from_url(picture)
                profile.save()
            return redirect('userprofile_page')
        else:
            print("Не удалось войти через Google. Попробуйте еще раз")
            # return JsonResponse({"error": "Не удалось войти через Google. Попробуйте еще раз"}, status=403)
    else:
        url = "https://accounts.google.com/o/oauth2/auth?client_id=%s&response_type=code&scope=%s&redirect_uri=%s&state=google"
        scope = [
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email"
        ]
        scope = " ".join(scope)
        url = url % (settings.GP_CLIENT_ID, scope, redirect_uri)
        return redirect(url)


# страница редактирования данных пользователя
@login_required
def userprofile_page(request):
    user = request.user
    if request.method == "POST":
        user_name = request.POST['user_name']
        user_surname = request.POST['user_surname']
        user_niсkname = request.POST['user_niсkname']
        user_country = request.POST['user_country']
        user_city = request.POST['user_city']
        profile = UserProfile.objects.get(user=user)
        user = User.objects.get(id=user.id)
        try:
            user_avatar = request.FILES['avatar']
            profile.avatar = user_avatar
            profile.name = user_niсkname
            profile.country = user_country
            profile.city = user_city
            user.first_name = user_name
            user.last_name = user_surname
            user.save()
            profile.save()
        except:
            profile.name = user_niсkname
            profile.country = user_country
            profile.city = user_city
            user.first_name = user_name
            user.last_name = user_surname
            user.save()
            profile.save()
        return redirect('userprofile_page')
    else:
        return render(request, 'accounts/editing_account.html', context={'first_name': user.first_name, 'last_name': user.last_name, \
                                                                     'niсkname': user.userprofile.name, 'country': user.userprofile.country, \
                                                                     'city': user.userprofile.city, 'reg_date': user.date_joined, \
                                                                     'avatar': user.userprofile.avatar})


# функция удаления аккаунта пользователя
@login_required
def delete_account(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_id2 = int(user_id)
        User.objects.filter(id=user_id2).delete()
        return JsonResponse({"success": "Delete account successfully!"}, status=200)
    else:
        raise Http404


# временная функция для создания UserProfile для ранее созданных пользователей (удалить вместе с url после однократного использования на проде)
def add_missing_profiles(request):
    users = User.objects.all()
    for user in users:
        created = UserProfile.objects.get_or_create(user=user)
        print(user.username, ' : ', created)
    print("all done")
    return HttpResponse("It's done.")


# выводит избранные курорты на страницу личного кабинета
@login_required
def favorites(request):
    user = request.user
    resorts = user.user.all()
    html = render_to_string('accounts/favorites_resorts.html', context={'resorts': resorts})
    return JsonResponse(html, safe=False)

# выводит отзывы пользователя и форму добавления отзыва на страницу личного кабинета
@login_required
def user_reviews(request):
    user = request.user
    reviews = SkiReview.objects.filter(author=user)
    return render(request, 'accounts/reviews_account.html', context={'reviews': reviews})