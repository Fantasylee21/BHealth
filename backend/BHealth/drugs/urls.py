from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from drugs.views import DrugView
from users.views import SendEmailRegisterCodeView, RigisterView, LoginView, AvatarView,DoctorView

urlpatterns = [
    path("drugs/", DrugView.as_view({'get': 'get', 'post': 'post','put':'delet_by_diagnosis'}), name='drugs'),
    path("drugs/<int:id>", DrugView.as_view({'put': 'put'}), name='drug'),
]
