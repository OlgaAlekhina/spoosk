from django.contrib.auth.models import User
from .models import UserProfile, SignupCode
from django.http import JsonResponse, HttpResponse, Http404
from rest_framework import viewsets, mixins
from .serializers import UserSerializer, UserprofileSerializer, LoginSerializer, CodeSerializer
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics
from datetime import timedelta, timezone
from rest_framework.decorators import action


class LoginAPIView(generics.GenericAPIView):
    """This api will handle login and return token for authenticate user."""
    # permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                token = Token.objects.get(user=user)
                response = {
                       "status": status.HTTP_200_OK,
                       "message": "success",
                       "data": {
                               "Token" : token.key
                               }
                       }
                return Response(response, status=status.HTTP_200_OK)
            else :
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


# endpoints for users
class UserViewset(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    list:

    """
    queryset = User.objects.all()
    http_method_names = [m for m in viewsets.ModelViewSet.http_method_names if m not in ['put']]
    parser_classes = (JSONParser, MultiPartParser)

    # add different serializers to list and detail view
    def get_serializer_class(self):
        if self.action == 'create':
            return UserSerializer
        elif self.action == 'verify_code':
            return CodeSerializer
        else:
            return UserprofileSerializer

    @action(detail=True, methods=['post'])
    def verify_code(self, request, pk=None):
        data = request.data
        code = data.get('code')
        print(code)
        user = self.get_object()
        print(user)
        # try:
        if SignupCode.objects.filter(code=code, user=user).exists():
            # signup_code = SignupCode.objects.get(code=code, user=user)
            # print(signup_code)
            # if signup_code.code_time - timezone.now() < timedelta(minutes=5):
            user.is_active = True
            user.save()
            token = Token.objects.get(user=user)
            response = {
                "status": status.HTTP_200_OK,
                "message": "Код подтвержден",
                "data": {
                    "Token": token.key
                }
            }
            return Response(response, status=status.HTTP_200_OK)
            # else:
            #     response = {
            #         "status": status.HTTP_400_BAD_REQUEST,
            #         "message": "Код устарел",
            #     }
            #     return Response(response, status=status.HTTP_400_BAD_REQUEST)
        # except:
        else:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Код введен неверно",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


# endpoint for code verification
# class CodeAPIView(generics.GenericAPIView):
#     serializer_class = CodeSerializer
#
#     def post(self, request):
#         data = request.data
#         code = data.get('code')
#         user = data.get('user')
#         try:
#             signup_code = SignupCode.objects.get(code=code, user=user)
#             if signup_code.code_time - timezone.now() < timedelta(minutes=5):
#                 user.is_active = True
#                 user.save()
#                 token = Token.objects.get(user=user)
#                 response = {
#                     "status": status.HTTP_200_OK,
#                     "message": "Код подтвержден",
#                     "data": {
#                         "Token": token.key
#                     }
#                 }
#                 return Response(response, status=status.HTTP_200_OK)
#             else:
#                 response = {
#                     "status": status.HTTP_400_BAD_REQUEST,
#                     "message": "Код устарел",
#                 }
#                 return Response(response, status=status.HTTP_400_BAD_REQUEST)
#         except:
#             response = {
#                 "status": status.HTTP_400_BAD_REQUEST,
#                 "message": "Код введен неверно",
#             }
#             return Response(response, status=status.HTTP_400_BAD_REQUEST)


# временная функция для создания UserProfile для ранее созданных пользователей (удалить вместе с url после однократного использования на проде)
def add_missing_profiles(request):
    users = User.objects.all()
    for user in users:
        created = UserProfile.objects.get_or_create(user=user)
        print(user.username, ' : ', created)
    print("all done")
    return HttpResponse("It's done.")

