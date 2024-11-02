import re
from datetime import datetime

from django.contrib.admin import filters
from django.core.cache import cache
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
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
        code = request.data.get('code')
        type = request.data.get('type')
        # try:
        #     try:
        #         tmp = EmailVerifyRecord.objects.get(email=email)
        #     except MultipleObjectsReturned:
        #         # 处理多个结果的情况
        #         tmps = EmailVerifyRecord.objects.filter(email=email)
        #         # 例如，选择最新的记录
        #         tmp = tmps.order_by('-send_time').first()
        # except EmailVerifyRecord.DoesNotExist:
        #     return Response({"error": "验证码不存在"}, status=status.HTTP_400_BAD_REQUEST)
        cache_key = f'verification_code:{email}'
        saved_code = cache.get(cache_key)

        if saved_code != code:
            return Response({"error": "验证码错误"}, status=status.HTTP_400_BAD_REQUEST)
        if not all([username, email, password, code]):
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "用户邮箱已注册"}, status=status.HTTP_400_BAD_REQUEST)
        if re.search(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email) is None:
            return Response({"error": "邮箱格式错误"}, status=status.HTTP_400_BAD_REQUEST)
        # tmp.delete()
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


class SendEmailRetrieveCodeView(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        data = {
            'error_email': ''
        }
        if not email:
            return Response({"error": "邮箱不能为空"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_obj = models.User.objects.filter(email=email, is_active=True).first()
            if not user_obj:
                data['error_email'] = "用户不存在"
                return Response(data, status=status.HTTP_404_NOT_FOUND)
            else:
                res_email = send_code_email(email, send_type="retrieve")
                if res_email:
                    return Response(status=status.HTTP_200_OK)
                else:
                    data['error_email'] = "验证码发送失败, 请稍后重试"
                    return Response(data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("错误信息 : ", e)
            data['error_email'] = e.__str__()
        return Response(data, status=status.HTTP_404_NOT_FOUND)


class RetrieveView(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        code = request.data.get('code')
        if not all([email, password, code]):
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        cache_key = f'verification_code:{email}'
        saved_code = cache.get(cache_key)
        if saved_code != code:
            return Response({"error": "验证码错误"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "用户不存在"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save()
        return Response(status=status.HTTP_200_OK)


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
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
        # print(avatar)
        if not avatar:
            return Response({"error": "头像不能为空"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not avatar.name.endswith('.jpg') and not avatar.name.endswith('.png'):
            return Response({"error": "头像格式错误"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if avatar.size > 1024 * 1024 * 2:
            return Response({"error": "头像过大"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        serializer = self.get_serializer(obj, data={"avatar": avatar}, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"url": serializer.data['avatar']}, status=status.HTTP_200_OK)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # 设置每页显示的记录数为10
    page_size_query_param = 'page_size'  # 允许通过查询参数来控制每页的记录数
    max_page_size = 100  # 设置最大页大小，防止过大的请求


class DoctorView(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, UserPermission]
    pagination_class = StandardResultsSetPagination  # 使用上面定义的分页类

    # 页的大小变为10
    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(type='doctor').order_by('id')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_single_doctor(self, request, *args, **kwargs):
        doctor = self.get_object()
        serializer = self.get_serializer(doctor, context={'request': request})
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
        serializer = self.get_serializer(doctor, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def write_diagnosis(self, request, *args, **kwargs):
        doctor = self.request.user
        patient = self.get_object()
        time = datetime.now().strftime("%Y-%m-%d %H:%M")
        app = Appointment.objects.filter(doctor=doctor, user=patient, from_time__lte=time, end_time__gt=time).first()
        if not app:
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
        serializer = self.get_serializer(doctors, many=True, context={'request': request})
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
        if from_time > end_time:
            return Response({"error": "开始时间不能晚于结束时间"}, status=status.HTTP_400_BAD_REQUEST)
        if WorkSchedule.objects.filter(doctor=doctor, from_time=from_time, end_time=end_time).exists():
            return Response({"error": "该时间段已存在"}, status=status.HTTP_400_BAD_REQUEST)
        ws = WorkSchedule.objects.create(doctor=doctor, from_time=from_time, end_time=end_time, num=num)
        serializer = WorkScheduleSerializer(ws)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientView(GenericViewSet):
    queryset = User.objects.all()

    # 分页
    @action(methods=['get'], detail=True, permissions=[NotPatientPermission])
    def get_patients(self, request, *args, **kwargs):
        patients = User.objects.filter(type='patient')
        page = self.paginate_queryset(patients)
        if page is not None:
            serializer = UserSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = UserSerializer(patients, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_single_patient(self, request, *args, **kwargs):
        patient = self.get_object()
        serializer = UserSerializer(patient, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def upload_appointment(self, request, *args, **kwargs):
        patient = self.request.user
        doctor_id = request.data.get('doctor_id')
        doctor = User.objects.get(id=doctor_id)
        if doctor.type != 'doctor':
            return Response({"error": "该用户不是医生"}, status=status.HTTP_400_BAD_REQUEST)
        from_time = request.data.get('from_time')
        end_time = request.data.get('end_time')
        if not all([doctor_id, from_time, end_time]):
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        # workSchedule = WorkSchedule.objects.filter(doctor=doctor)
        workSchedule = WorkSchedule.objects.filter(doctor=doctor, from_time=from_time, end_time=end_time)
        if Appointment.objects.filter(doctor=doctor, from_time=from_time, end_time=end_time).exists():
            return Response({"error": "该时间段你已预约"}, status=status.HTTP_400_BAD_REQUEST)
        if not workSchedule or workSchedule[0].num <= 0:
            return Response({"error": "该时间段医生不在工作或预约名额不足"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            workSchedule[0].num -= 1
            workSchedule[0].save()
        appointment = models.Appointment.objects.create(user=patient, doctor=doctor, from_time=from_time,
                                                        end_time=end_time)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
        education = request.data.get('education')
        title = request.data.get('title')
        work_time = request.data.get('work_time')
        school = request.data.get('school')

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
        if education:
            user.education = education
        if title:
            user.title = title
        if work_time:
            user.work_time = work_time
        if school:
            user.school = school
        user.save()
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
