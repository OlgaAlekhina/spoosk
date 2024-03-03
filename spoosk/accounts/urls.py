from django.urls import path
from .views import signup_endpoint, login_endpoint, signup_confirmation, reset_request, reset_confirmation, reset_endpoint,\
                    google_login, userprofile_page, delete_account, user_favorites, add_missing_profiles, user_reviews, edit_review, delete_review
from resorts.views import add_resort, review_submit
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
    path('google-login', google_login, name='google_login'),
    path('profile/', userprofile_page, name='userprofile_page'),
    path('delete_account/', delete_account, name='delete_account'),
    path('add_resort/<str:pk>/', add_resort, name='add_resort'),
    path('favorites/', user_favorites, name='favorites'),
    path('add_missing_profiles/', add_missing_profiles, name='add_missing_profiles'),
    path('user_reviews/', user_reviews, name='user_reviews'),
    path('review_submit/', review_submit, name='review_submit'),
    path('edit_review/<str:pk>/', edit_review, name='edit_review'),
    path('delete_review/<str:pk>/', delete_review, name='delete_review'),
]