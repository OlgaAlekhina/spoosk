from .models import UserProfile, SignupCode
from rest_framework import viewsets, mixins, status
from .serializers import UserSerializer, UserprofileSerializer, LoginSerializer, CodeSerializer, ResetpasswordSerializer, ChangepasswordSerializer, EmptySerializer
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from resorts.models import SkiResort, SkiReview, ReviewImage
from rest_framework.authtoken.models import Token
from resorts.serializers import SkireviewSerializer, ResortSerializer
from rest_framework.response import Response
from spoosk.permissions import APIkey, UserPermission
from datetime import timedelta
from django.utils import timezone
from rest_framework.decorators import action
from random import randint
from django.shortcuts import get_object_or_404
from django.db.models import OuterRef, Exists
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import user_token
import json
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
import requests


# аутентификация пользователя по мейлу
def authenticate_user(email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    else:
        if user.check_password(password) and user.is_active:
            return user
    return None


# endpoints for users
class UserViewset(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    create: Эндпоинт для регистрации, принимает имя, email и пароль пользователя и при успешной регистрации возвращает его данные, включая id.
            Полученный id следует передать в эндпоинте api/users/verify_code для верификации введенного пользователем кода.
            При регистрации email проверяется на уникальность и в случае несоответствия выдается ошибка.
    login: Эндпоинт для логина, принимает email и пароль пользователя и при успешной аутентификации возвращает его токен.
    retrieve: Эндпоинт для получения личных данных пользователя по его id.
    verify_code: Эндпоинт для верификации высланного при регистрации кода, принимает id пользователя и код и при успешной проверке возвращает токен пользователя.
                 Код работает в течение 1 часа, после чего выдается ошибка "код устарел".
    reset_password_request: Эндпоинт для восстановления пароля, принимает email пользователя и при наличии такого объекта в БД возвращает его id.
                            Полученный id следует передать в эндпоинте api/users/verify_code для верификации введенного пользователем кода.
                            Если email не найден в БД, выдается ошибка.
    change_password: Эндпоинт для смены пароля, принимает новый пароль и id пользователя и возвращает его токен.
    send_code: Принимает id пользователя и высылает код подтверждения на его почтовый адрес.
    partial_update: Эндпоинт для редактирования личных данных пользователя по его id. В теле запроса можно передавать только те поля, которые подлежат изменению.
                    Загрузку файла (аватар) нет возможности протестировать в сваггере, пожалуйста, используйте postman для тестов.
                    Поле "avatar" может содержать только объект файла (а не его url). Если пользователь хочет удалить свою аватарку, в запросе надо передать поле "avatar" без значения.
    delete: Эндпоинт для удаления пользователя по его id.
    reviews: Эндпоинт для получения всех отзывов пользователя по его id. Выводится по 6 отзывов на страницу, отсортированных по дате создания. Запрос может включать номер страницы в качестве параметра.
             Пример: /api/users/{id}/reviews/?page=2
    favorites: Эндпоинт для получения списка курортов, добавленных в избранное пользователем, по его id.
    """
    queryset = User.objects.all()
    http_method_names = [m for m in viewsets.ModelViewSet.http_method_names if m not in ['put']]
    parser_classes = (JSONParser, MultiPartParser)
    permission_classes = [APIkey, UserPermission]

    # add different serializers to different actions
    def get_serializer_class(self):
        if self.action == 'create':
            return UserSerializer
        elif self.action == 'verify_code':
            return CodeSerializer
        elif self.action == 'reset_password_request':
            return ResetpasswordSerializer
        elif self.action == 'change_password':
            return ChangepasswordSerializer
        elif self.action == 'login':
            return LoginSerializer
        elif self.action == 'send_code':
            return EmptySerializer
        elif self.action == 'reviews':
            return SkireviewSerializer
        elif self.action == 'favorites':
            return ResortSerializer
        else:
            return UserprofileSerializer

    def get_active_user(self):
        user = get_object_or_404(User, pk=self.kwargs["pk"], is_active=True)
        self.check_object_permissions(self.request, user)
        return user

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, pk=pk, is_active=True)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        data = request.data
        user = self.get_active_user()
        profile = user.userprofile
        print("Данные: ", data)
        if 'avatar' in data and data.get('avatar') == '':
            profile.avatar = None
            profile.save()
            print('delete avatar')
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            user.first_name = serializer.validated_data.get('first_name', user.first_name)
            user.last_name = serializer.validated_data.get('last_name', user.last_name)
            user.save()
            if 'userprofile' in serializer.validated_data:
                profile_data = serializer.validated_data.pop('userprofile')
                profile.name = profile_data.get('name', profile.name)
                profile.city = profile_data.get('city', profile.city)
                profile.country = profile_data.get('country', profile.country)
                profile.save()
            avatar = request.FILES.getlist("avatar")
            if len(avatar) != 0:
                profile.avatar = avatar[0]
                profile.save()

            response = {
                "message": "Профиль успешно обновлен",
                "data": {
                            "id": user.id,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "nickname": profile.name,
                            "city": profile.city,
                            "country": profile.country,
                            "avatar": profile.avatar.name
                        }
            }
            return Response(response)
        return Response(serializer.errors)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate_user(email=email, password=password)
            if user is not None:
                token = Token.objects.get(user=user)
                response = {
                    "status": status.HTTP_200_OK,
                    "message": "Авторизация прошла успешно",
                    "data": {
                        "id": user.id,
                        "Token": token.key
                    }
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "Неправильно введены учетные данные",
                }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def verify_code(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            user = self.get_object()
            if SignupCode.objects.filter(code=code, user=user).exists():
                signup_code = SignupCode.objects.get(code=code, user=user)
                if timezone.now() - signup_code.code_time < timedelta(minutes=60):
                    user.is_active = True
                    user.save()
                    signup_code.delete()
                    token = Token.objects.get(user=user)
                    response = {
                        "status": status.HTTP_200_OK,
                        "message": "Код подтвержден",
                        "data": {
                            "id": user.id,
                            "Token": token.key
                        }
                    }
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    response = {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Код устарел",
                    }
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Код введен неверно",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def reset_password_request(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            code = SignupCode.objects.create(code=randint(1000, 9999), user=user)
            msg = EmailMultiAlternatives(
                subject='Восстановление пароля в приложении Spoosk',
                from_email='spoosk.info@gmail.com',
                to=[user.email, ]
            )
            html_content = render_to_string(
                'accounts/reset_password_code.html',
                {'code': code.code,
                 'name': user.first_name}
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            response = {
                "status": status.HTTP_200_OK,
                "message": "success",
                "data": {
                    "id": user.id,
                    "email": user.email
                }
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        user = self.get_object()
        if user.is_superuser:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Нельзя редактировать данные этого пользователя",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            user.set_password(password)
            user.save()
            token = Token.objects.get(user=user)
            response = {
                "status": status.HTTP_200_OK,
                "message": "success",
                "data": {
                    "Token": token.key
                }
            }
            return Response(response, status=status.HTTP_200_OK)

        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def send_code(self, request, pk=None):
        user = self.get_object()
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
        response = {
            "status": status.HTTP_200_OK,
            "message": "Код подтверждения отправлен",
            "data": {
                "id": user.id,
                "email": user.email
            }
        }
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True)
    def reviews(self, request, pk=None):
        user = self.get_object()
        reviews = user.skireview_set.all().order_by('-add_at')
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(page, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def favorites(self, request, pk=None):
        user = self.get_object()
        favorites = user.user.all().annotate(in_favorites=Exists(SkiResort.objects.filter(id_resort=OuterRef("pk"), users=user))).order_by('name')
        page = self.paginate_queryset(favorites)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(page, many=True)
        return Response(serializer.data)


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
def user_favorites(request):
    user = request.user
    resorts = user.user.all()
    html = render_to_string('accounts/favorites_resorts.html', context={'resorts': resorts})
    return JsonResponse(html, safe=False)


# выводит отзывы пользователя и форму добавления отзыва на страницу личного кабинета
@login_required
def user_reviews(request):
    user = request.user
    reviews = SkiReview.objects.filter(author=user).order_by('approved', '-add_at')
    return render(request, 'accounts/reviews_account.html', context={'reviews': reviews})


# endpoint for editing review
def edit_review(request, pk):
    if request.method == "POST":
        review = SkiReview.objects.get(id=pk)
        review.text = request.POST.get('text')
        review.rating = request.POST.get('rating')
        review.save()
        for image in request.POST.getlist('images_del'):
            ReviewImage.objects.filter(id=int(image)).delete()
        for image in request.FILES.getlist('images'):
            ReviewImage.objects.create(image=image, review=review)
        return JsonResponse({"success": "Edit review successfully!"}, status=200)
    else:
        raise Http404


# delete review from database
def delete_review(request, pk):
    if request.method == "DELETE":
        SkiReview.objects.filter(id=pk).delete()
        return JsonResponse({"success": "Delete review successfully!"}, status=200)
    else:
        raise Http404