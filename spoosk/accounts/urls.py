from django.urls import path
from .views import signup_endpoint, login_endpoint, signup_confirmation, reset_request, reset_confirmation, reset_endpoint,\
                    userprofile_page, add_missing_profiles
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='resorts', permanent=True)),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup_endpoint/', signup_endpoint, name='signup_endpoint'),
    path('login_endpoint/', login_endpoint, name='login_endpoint'),
    path('signup_confirmation/<uidb64>/<token>', signup_confirmation, name='signup_confirmation'),
    path('reset_request/', reset_request, name='reset_request'),
    path('reset_confirmation/', reset_confirmation, name='reset_confirmation'),
    path('reset_endpoint/', reset_endpoint, name='reset_endpoint'),
    path('profile/', userprofile_page, name='userprofile_page'),
    path('add_missing_profiles/', add_missing_profiles, name='add_missing_profiles'),
]