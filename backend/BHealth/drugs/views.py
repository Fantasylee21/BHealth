import json

from rest_framework.views import APIView

from drugs.models import Drug
from drugs.serializers import DrugSerializer
from permisson import UserPermission, NotPatientPermission, YaoshiPermission
from users import models
from users.models import User, EmailVerifyRecord, Diagnosis
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
class DrugView(GenericViewSet):
    serializer_class = DrugSerializer
    permission_classes = [YaoshiPermission]

    def get(self, request, *args, **kwargs):
        drugs = Drug.objects.all()
        page = self.paginate_queryset(drugs)
        if page is not None:
            serializer = DrugSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = DrugSerializer(drugs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = DrugSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        drug = Drug.objects.get(id=kwargs['id'])
        data = request.data
        serializer = DrugSerializer(drug, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_by_name(self, request, *args, **kwargs):
        name = kwargs['name']
        drugs = Drug.objects.filter(name=name)
        serializers = DrugSerializer(drugs, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def delet_by_diagnosis(self, request, *args, **kwargs):
        userid = request.data.get('userid')
        patient = User.objects.get(id=userid)
        diagnosis =patient.diagnosis.filter(is_taken=False).order_by('-create_time').first().content
        a=type(diagnosis)
        diagnosis = json.loads(diagnosis.replace("'", '"'))
        takenDrugs = diagnosis['takenDrugs']
        account = 0
        for takendrug in takenDrugs:
            if takendrug[1] < 0:
                return Response({'error': '数量不能为负数'}, status=status.HTTP_400_BAD_REQUEST)
            drug = Drug.objects.get(name=takendrug[0])
            if drug.stock < takendrug[1]:
                return Response({f'error': f'库存{drug}不足,剩余量为{drug.stock}'}, status=status.HTTP_400_BAD_REQUEST)
        for takendrug in takenDrugs:
            drug = Drug.objects.get(name=takendrug[0])
            drug.stock -= takendrug[1]
            drug.save()
            account += drug.price * takendrug[1]
        return Response({'account': account}, status=status.HTTP_200_OK)
