from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet

from news.models import News
from news.serializers import NewsSerializer
from news.unit import ask
from permisson import SuperUserPermission
import re

from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, viewsets
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

class NewsView(GenericViewSet):
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]
    queryset = News.objects.all()

    def get(self, request, *args, **kwargs):
        news = News.objects.all()
        page = self.paginate_queryset(news)
        if page is not None:
            serializer = NewsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, permission_classes=[SuperUserPermission])
    def post(self, request, *args, **kwargs):
        title = request.data.get('title')
        content = request.data.get('content')
        front_image = request.data.get('front_image')
        discretion = request.data.get('discretion')
        type = request.data.get('type')
        if not all([title, content, discretion]):
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        news = News.objects.create(title=title, content=content, front_image=front_image, discretion=discretion,type = type)
        serializer = NewsSerializer(news)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['put'], detail=False, permission_classes=[SuperUserPermission])
    def delete(self, request, *args, **kwargs):
        news = self.get_object()
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_by_id(self, request, *args, **kwargs):
        news = self.get_object()
        serializer = NewsSerializer(news)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AiViewSet(viewsets.ModelViewSet):
    def ask(self, request, *args, **kwargs):
        content = request.data.get('content')
        if not content:
            return Response({'error': '缺少content参数'}, status=400)

        res = ask(content)
        return Response({'result': res}, status=200)
