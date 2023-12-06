from django.contrib import admin
from .models import UserProfile, SignupCode

admin.site.register(UserProfile)
admin.site.register(SignupCode)

