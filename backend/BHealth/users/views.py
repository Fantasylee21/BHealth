import re
from datetime import datetime

from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from BHealth.settings import MEDIA_ROOT
from permisson import UserPermission, NotPatientPermission, SuperUserPermission
from users import models
from users.models import User, EmailVerifyRecord, WorkSchedule, Diagnosis, Appointment
from users.send_email import send_code_email
from users.serializers import UserSerializer, DoctorSerializer, AppointmentSerializer, WorkScheduleSerializer
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
        # passwordConfirm = request.data.get('passwordconfirm')
        code = request.data.get('code')
        type = request.data.get('type')
        # category = request.data.get('category')
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
        if not all([username, email, password, code]):
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "用户邮箱已注册"}, status=status.HTTP_400_BAD_REQUEST)

        # if password != passwordConfirm:
        #     return Response({"error": "两次密码不一致"}, status=status.HTTP_400_BAD_REQUEST)

        # 校验密码强度
        # if not 6 < len(password) < 18:
        #     return Response({"error": "密码长度不在要求范围内"}, status=status.HTTP_400_BAD_REQUEST)
        # 匹配邮箱
        if re.search(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email) is None:
            return Response({"error": "邮箱格式错误"}, status=status.HTTP_400_BAD_REQUEST)
        tmp.delete()
        # if category:
        #     user = User.objects.create_user(username=username, email=email, password=password, type=type,
        #                                     category=category)
        # else:
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
    permission_classes = [IsAuthenticated, UserPermission, SuperUserPermission]

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
        doctors = User.objects.filter(type='doctor')
        # doctors = User.objects.all()
        page = self.paginate_queryset(doctors)
        if page is not None:
            serializer = DoctorSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_single_doctor(self, request, *args, **kwargs):
        doctor = self.get_object()
        serializer = self.get_serializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, permissions=[NotPatientPermission])
    def post(self, request, *args, **kwargs):
        doctor = self.get_object()
        introduction = request.data.get('introduction')
        if doctor.type != 'doctor':
            return Response({"error": "该用户不是医生"}, status=status.HTTP_400_BAD_REQUEST)
        if introduction:
            doctor.introduction = introduction
        doctor.save()
        return Response(status=status.HTTP_200_OK)

    def write_diagnosis(self, request, *args, **kwargs):
        doctor = self.request.user
        patient = self.get_object()
        time = datetime.now().strftime("%Y-%m-%d %H:%M")
        app = Appointment.objects.filter(doctor=doctor, patient=patient, time__lte=time).first()
        if not app.exists():
            return Response({"error": "未进行预约"}, status=status.HTTP_400_BAD_REQUEST)
        # 删除这条预约
        app.delete()
        diagnosis = Diagnosis.objects.create(doctor=doctor, patient=patient, content=request.data.get('content'))
        return Response(status=status.HTTP_201_CREATED)

    def get_special_doctors(self, request, *args, **kwargs):
        name = request.GET.get('name')
        category = request.GET.get('category')
        content = request.GET.get('content')
        doctors = User.objects.filter(type='doctor')
        if name:
            doctors = doctors.filter(username=name)
        if category:
            doctors = doctors.filter(category=category)
        if content:
            doctors = doctors.filter(introduction__contains=content)
        serializer = self.get_serializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, permissions=[NotPatientPermission])
    def upload_workSchedule(self, request, *args, **kwargs):
        doctor = self.get_object()
        from_time = request.data.get('from_time')
        end_time = request.data.get('end_time')
        num = request.data.get('num')
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        if not all([from_time, end_time, num]):
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        if (from_time < now_time) or (end_time < now_time):
            return Response({"error": "时间不能早于当前时间"}, status=status.HTTP_400_BAD_REQUEST)
        if from_time < end_time:
            return Response({"error": "开始时间不能晚于结束时间"}, status=status.HTTP_400_BAD_REQUEST)
        if WorkSchedule.objects.filter(doctor=doctor, from_time=from_time, end_time=end_time).exists():
            return Response({"error": "该时间段已存在"}, status=status.HTTP_400_BAD_REQUEST)
        ws = WorkSchedule.objects.create(doctor=doctor, from_time=from_time, end_time=end_time, num=num)
        serializer = WorkScheduleSerializer(ws)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_appointment(self, request, *args, **kwargs):
        doctor = self.request.user
        appointments = models.Appointment.objects.filter(doctor=doctor)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientView(GenericViewSet):
    queryset = User.objects.all()

    # 分页
    @action(methods=['get'], detail=True, permissions=[NotPatientPermission])
    def get_patients(self, request, *args, **kwargs):
        patients = User.objects.filter(type='patient')
        page = self.paginate_queryset(patients)
        if page is not None:
            serializer = UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UserSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_single_patient(self, request, *args, **kwargs):
        patient = self.get_object()
        serializer = UserSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def upload_appointment(self, request, *args, **kwargs):
        patient = self.request.user
        doctor_id = request.data.get('doctor_id')
        doctor = User.objects.get(id=doctor_id)
        if doctor.type != 'doctor':
            return Response({"error": "该用户不是医生"}, status=status.HTTP_400_BAD_REQUEST)
        time = request.data.get('time')
        if not time:
            return Response({"error": "时间不能为空"}, status=status.HTTP_400_BAD_REQUEST)
        # workSchedule = WorkSchedule.objects.filter(doctor=doctor)
        workSchedule = WorkSchedule.objects.filter(doctor=doctor).filter(from_time__lte=time).filter(end_time__gte=time)
        if not workSchedule or workSchedule[0].num <= 0:
            return Response({"error": "该时间段医生不在工作或预约名额不足"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            workSchedule[0].num -= 1
            workSchedule[0].save()
        appointment = models.Appointment.objects.create(patient=patient, doctor=doctor, time=time)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_appointment(self, request, *args, **kwargs):
        patient = self.request.user
        appointments = models.Appointment.objects.filter(patient=patient)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FileView(APIView):
    """获取文件的视图"""

    def get(self, request, name):
        path = os.path.join(MEDIA_ROOT, name)
        if os.path.isfile(path):
            return FileResponse(open(path, 'rb'))
        return Response({'error': "没有找到该文件"}, status=status.HTTP_404_NOT_FOUND)


class UserView(GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def put(self, request, *args, **kwargs):
        u = self.request.user
        if not (u.is_superuser or u.id == self.get_object().id):
            return Response({"error": "没有权限"}, status=status.HTTP_403_FORBIDDEN)
        user = self.get_object()
        username = request.data.get('username')
        email = request.data.get('email')
        type = request.data.get('type')
        category = request.data.get('category')
        introduction = request.data.get('introduction')

        if username:
            user.username = username
        if email:
            user.email = email
        if type:
            user.type = type
        if category:
            user.category = category
        if introduction:
            user.introduction = introduction
        user.save()
        return Response(status=status.HTTP_200_OK)
