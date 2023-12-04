from django.contrib.auth.models import User
from .models import UserProfile
from django.http import JsonResponse, HttpResponse, Http404


# временная функция для создания UserProfile для ранее созданных пользователей (удалить вместе с url после однократного использования на проде)
def add_missing_profiles(request):
    users = User.objects.all()
    for user in users:
        created = UserProfile.objects.get_or_create(user=user)
        print(user.username, ' : ', created)
    print("all done")
    return HttpResponse("It's done.")

