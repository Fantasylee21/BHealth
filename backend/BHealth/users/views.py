import re

from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from permisson import UserPermission, NotPatientPermission
from users import models
from users.models import User, EmailVerifyRecord
from users.send_email import send_code_email
from users.serializers import UserSerializer, DoctorSerializer
import os
import random
import re

from django.core.mail import send_mail
from django.http import FileResponse
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle


# Create your views here.
class RigisterView(APIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        passwordConfirm = request.data.get('passwordconfirm')
        code = request.data.get('code')
        type = request.data.get('type')
        try:
            tmp = EmailVerifyRecord.objects.get(email=email)
        except MultipleObjectsReturned:
            # 处理多个结果的情况
            tmps = EmailVerifyRecord.objects.filter(email=email)
            # 例如，选择最新的记录
            tmp = tmps.order_by('-send_time').first()
        if tmp.code != code:
            return Response({"error": "验证码错误"}, status=status.HTTP_400_BAD_REQUEST)
        # print(username, email, password, passwordConfirm)
        if not all([username, email, password, passwordConfirm, code]):
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "用户邮箱已注册"}, status=status.HTTP_400_BAD_REQUEST)

        if password != passwordConfirm:
            return Response({"error": "两次密码不一致"}, status=status.HTTP_400_BAD_REQUEST)

        # 校验密码强度
        if not 6 < len(password) < 18:
            return Response({"error": "密码长度不在要求范围内"}, status=status.HTTP_400_BAD_REQUEST)
        # 匹配邮箱
        if re.search(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email) is None:
            return Response({"error": "邮箱格式错误"}, status=status.HTTP_400_BAD_REQUEST)
        tmp.delete()
        user = User.objects.create_user(username=username, email=email, password=password, type=type)
        result = {
            "username": user.username,
            "email": user.email,
            "id": user.id,
            "type": user.type
        }
        return Response(result, status=status.HTTP_201_CREATED)


class SendEmailRegisterCodeView(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        data = {
            'error_email': ''
        }
        if not email:
            return Response({"error": "邮箱不能为空"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_obj = models.User.objects.filter(email=email, is_active=True).first()
            if user_obj:
                data['error_email'] = "用户已存在"
                return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                res_email = send_code_email(email, send_type="register")
                if res_email:
                    return Response(status=status.HTTP_200_OK)
                else:
                    data['error_email'] = "验证码发送失败, 请稍后重试"
                    return Response(data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("错误信息 : ", e)
            data['error_email'] = e.__str__()
        return Response(data, status=status.HTTP_404_NOT_FOUND)


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"error": "用户名或密码错误"}, status=status.HTTP_400_BAD_REQUEST)

        result = serializer.validated_data
        result['username'] = serializer.user.username
        result['id'] = serializer.user.id
        result['email'] = serializer.user.email
        result['token'] = result.pop('access')
        result['refresh'] = result.pop('refresh')
        result['type'] = serializer.user.type
        return Response(result, status=status.HTTP_200_OK)


class AvatarView(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserPermission]


    def avatar_upload(self, request, *args, **kwargs):
        obj = self.get_object()
        avatar = request.data.get('avatar')
        if not avatar:
            return Response({"error": "头像不能为空"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not avatar.name.endswith('.jpg') and not avatar.name.endswith('.png'):
            return Response({"error": "头像格式错误"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if avatar.size > 1024 * 300:
            return Response({"error": "头像过大"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        serializer = self.get_serializer(obj, data={"avatar": avatar}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"url": serializer.data['avatar']}, status=status.HTTP_200_OK)


class DoctorView(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, UserPermission]

    def get(self, request, *args, **kwargs):
        doctors = User.objects.filter(type='医生')
        serializer = self.get_serializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_single_doctor(self, request, *args, **kwargs):
        doctor = self.get_object()
        serializer = self.get_serializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, permissions=[NotPatientPermission])
    def post(self, request, *args, **kwargs):
        doctor = self.get_object()
        workSchedule = request.data.get('workSchedule')
        introduction = request.data.get('introduction')
        if doctor.type != '医生':
            return Response({"error": "该用户不是医生"}, status=status.HTTP_400_BAD_REQUEST)
        # 改变医生的时间表
        if workSchedule:
            doctor.workSchedule = workSchedule
        if introduction:
            doctor.introduction = introduction
        doctor.save()
        return Response(status=status.HTTP_200_OK)

    def write_diagnosis(self, request, *args, **kwargs):
        doctor = self.request.user
        patient = self.get_object()
        diagnosis = request.data.get('diagnosis')
        if doctor.type != '医生' and not doctor.is_superuser:
            return Response({"error": "该用户不是医生"}, status=status.HTTP_400_BAD_REQUEST)
        if not diagnosis:
            return Response({"error": "诊断记录不能为空"}, status=status.HTTP_400_BAD_REQUEST)

        patient.diagnosis = diagnosis
        patient.save()
        return Response(status=status.HTTP_200_OK)

