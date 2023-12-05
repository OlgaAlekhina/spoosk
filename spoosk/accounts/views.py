from django.contrib.auth.models import User
from .models import UserProfile
from django.http import JsonResponse, HttpResponse, Http404
from rest_framework import viewsets, mixins
from .serializers import UserSerializer, UserprofileSerializer
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser


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
        else:
            return UserprofileSerializer


# временная функция для создания UserProfile для ранее созданных пользователей (удалить вместе с url после однократного использования на проде)
def add_missing_profiles(request):
    users = User.objects.all()
    for user in users:
        created = UserProfile.objects.get_or_create(user=user)
        print(user.username, ' : ', created)
    print("all done")
    return HttpResponse("It's done.")

