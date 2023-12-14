from django.contrib.auth.models import User
from .models import UserProfile, SignupCode
from django.http import JsonResponse, HttpResponse, Http404
from rest_framework import viewsets, mixins
from .serializers import UserSerializer, UserprofileSerializer, LoginSerializer, CodeSerializer, ResetpasswordSerializer, ChangepasswordSerializer
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics
from datetime import timedelta
from django.utils import timezone
from rest_framework.decorators import action
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from random import randint


# user authentication by email and password
def authenticate_user(email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    else:
        if user.check_password(password) and user.is_active:
            return user
    return None


# class LoginAPIView(generics.GenericAPIView):
#     """ Эндпоинт для логина, принимает email и пароль пользователя и при успешной аутентификации возвращает его токен. """
#     serializer_class = LoginSerializer

    # def post(self, request):
    #     serializer = LoginSerializer(data=request.data)
    #     if serializer.is_valid():
    #         email = serializer.validated_data["email"]
    #         password = serializer.validated_data["password"]
    #         user = authenticate_user(email=email, password=password)
    #         if user is not None:
    #             token = Token.objects.get(user=user)
    #             response = {
    #                    "status": status.HTTP_200_OK,
    #                    "message": "Авторизация прошла успешно",
    #                    "data": {
    #                            "Token" : token.key
    #                            }
    #                    }
    #             return Response(response, status=status.HTTP_200_OK)
    #         else :
    #             response = {
    #                    "status": status.HTTP_401_UNAUTHORIZED,
    #                    "message": "Неправильно введены учетные данные",
    #                    }
    #             return Response(response, status=status.HTTP_401_UNAUTHORIZED)
    #     response = {
    #          "status": status.HTTP_400_BAD_REQUEST,
    #          "message": "bad request",
    #          "data": serializer.errors
    #          }
    #     return Response(response, status=status.HTTP_400_BAD_REQUEST)


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
    """
    queryset = User.objects.all()
    http_method_names = [m for m in viewsets.ModelViewSet.http_method_names if m not in ['put']]
    parser_classes = (JSONParser, MultiPartParser)

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
        else:
            return UserprofileSerializer

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
        data = request.data
        code = data.get('code')
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
        # except:
        else:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Код введен неверно",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def reset_password_request(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # data = request.data
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
                {'code': code.code}
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
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # data = request.data
            password = serializer.validated_data['password']
            user = self.get_object()
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


# временная функция для создания UserProfile для ранее созданных пользователей (удалить вместе с url после однократного использования на проде)
def add_missing_profiles(request):
    users = User.objects.all()
    for user in users:
        created = UserProfile.objects.get_or_create(user=user)
        print(user.username, ' : ', created)
    print("all done")
    return HttpResponse("It's done.")

