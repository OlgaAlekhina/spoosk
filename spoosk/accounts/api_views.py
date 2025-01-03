from .models import SignupCode
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
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


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
    create: Создает нового пользователя в базе данных. Принимает имя, email и пароль пользователя и при успешной регистрации возвращает его id.
            Полученный id следует передать в эндпоинте api/users/verify_code для верификации введенного пользователем кода.
            Регистрация разрешается, только если пользователя с таким email не существует в базе данных или его профиль не был активирован.
            Условия доступа к эндпоинту: APIkey
    login: Производит аутентификацию пользователя по email и паролю и в случае успеха возвращает его токен.
           Условия доступа к эндпоинту: APIkey
    retrieve: Выводит личные данные пользователя по его id.
              Условия доступа к эндпоинту: APIkey
    verify_code: Эндпоинт для верификации кода, высланного по email. Принимает id пользователя и код и при успешной проверке возвращает токен пользователя.
                 Код работает в течение 1 часа, после чего выдается ошибка "код устарел".
                 Условия доступа к эндпоинту: APIkey
    reset_password_request: Делает запрос на восстановление пароля. Принимает email пользователя и при наличии такого объекта в БД возвращает его id.
                            Полученный id следует передать в эндпоинте api/users/verify_code для верификации введенного пользователем кода.
                            Условия доступа к эндпоинту: APIkey
    change_password: Меняет пароль пользователя в базе данных. Принимает новый пароль и id пользователя и возвращает его токен.
                     Условия доступа к эндпоинту: APIkey, токен авторизации (пользователь может поменять пароль только в своем профиле)
    send_code: Принимает id пользователя и высылает код подтверждения на его почтовый адрес.
               Условия доступа к эндпоинту: APIkey
    partial_update: Осуществляет частичное редактирование личных данных пользователя по его id. В теле запроса можно передавать только те параметры, которые подлежат изменению.
                    Загрузку файла (аватар) нет возможности протестировать в сваггере, пожалуйста, используйте postman для тестов.
                    Параметр "avatar" может содержать только объект файла (а не его url). Если пользователь хочет удалить свою аватарку, в запросе надо передать параметр "avatar" без значения.
                    Условия доступа к эндпоинту: APIkey, токен авторизации (пользователь может редактировать только свой собственный профиль)
    delete: Удаляет учетную запись пользователя из базы данных по его id.
            Условия доступа к эндпоинту: APIkey, токен авторизации (пользователь может удалить только свой собственный профиль)
    reviews: Выводит все отзывы пользователя по его id. Выводится по 7 отзывов на страницу, отсортированных по дате создания. Запрос может включать номер страницы в качестве параметра.
             Пример: /api/users/{id}/reviews/?page=2
             Условия доступа к эндпоинту: APIkey
    favorites: Выводит список курортов, добавленных в избранное пользователем, по его id.
               Выводится по 7 курортов на страницу. Запрос может включать номер страницы в качестве параметра. Пример: /api/users/{id}/favorites/?page=2
               Условия доступа к эндпоинту: APIkey
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
        if 'avatar' in data and data.get('avatar') == '':
            profile.avatar = None
            profile.save()
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

