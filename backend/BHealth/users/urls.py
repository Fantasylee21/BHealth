"""
URL configuration for IQuizHub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from users.views import SendEmailRegisterCodeView, RigisterView, LoginView, AvatarView,DoctorView,PatientView

urlpatterns = [
    path('mail/', SendEmailRegisterCodeView.as_view(), name='send_email_register_code'),
    path('register/', RigisterView.as_view(), name='register'),
    path('login/',LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("token/verify/", TokenVerifyView.as_view(), name='token_verify'),
    path("<int:pk>/avatar/upload/", AvatarView.as_view({'post': 'avatar_upload'}), name='头像上传'),
    path('doctors/', DoctorView.as_view({'get': 'get'}), name='doctors'),
    path('doctors/<int:pk>', DoctorView.as_view({'get': 'get_single_doctor'}), name='doctor'),
    path('doctors/special/', DoctorView.as_view({'get': 'get_special_doctors'}), name='special_doctors'),
    path('doctors/<int:pk>', DoctorView.as_view({'post': 'post'}), name='doctor'),
    path('doctors/<int:pk>/workSchedule/', DoctorView.as_view({'post':'upload_workSchedule'}), name='workSchedule'),
    path('patients/', PatientView.as_view({'get': 'get_patients'}), name='patients'),
    path('patients/<int:pk>', PatientView.as_view({'get': 'get_single_patient'}), name='patient'),
    path('patients/<int:pk>/diagnosis', PatientView.as_view({'post': 'post'}), name='patient'),
    path('diagnosis/<int:pk>', DoctorView.as_view({'put': 'write_diagnosis'}), name='diagnosis'),
]
