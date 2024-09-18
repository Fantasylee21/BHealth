from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from users.views import SendEmailRegisterCodeView, RigisterView, LoginView, AvatarView,DoctorView,PatientView

urlpatterns = [
    # path('mail/',)
]