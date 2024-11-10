import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from drugs.models import Drug
from drugs.serializers import DrugSerializer
from permisson import YaoshiPermission
from users.models import User, Diagnosis


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
        if not drug:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.data.get('stock'):
            drug.stock = request.data.get('stock')
        if request.data.get('price'):
            drug.price = request.data.get('price')
        if request.data.get('name'):
            drug.name = request.data.get('name')
        if request.data.get('description'):
            drug.description = request.data.get('description')
        if request.data.get('dosage'):
            drug.image = request.data.get('dosage')
        drug.save()
        return Response(status=status.HTTP_200_OK)

    def get_by_name(self, request, *args, **kwargs):
        name = kwargs['name']
        drugs = Drug.objects.filter(name=name)
        serializers = DrugSerializer(drugs, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def delet_by_diagnosis(self, request, *args, **kwargs):
        userid = request.data.get('userid')
        patient = User.objects.get(id=userid)
        d = Diagnosis.objects.filter(patient=patient, is_taken=False).order_by('-create_time').first()
        # print(d.create_time)
        if not d:
            return Response({'error': '没有未取药的诊断'}, status=status.HTTP_400_BAD_REQUEST)
        diagnosis = d.content
        # a = type(diagnosis)
        diagnosis = json.loads(diagnosis.replace("'", '"'))
        takenDrugs = diagnosis['takenDrugs']
        account = 0
        for takendrug in takenDrugs:
            if takendrug[1] < 0:
                return Response({'error': '数量不能为负数'}, status=status.HTTP_400_BAD_REQUEST)
            if not Drug.objects.filter(name=takendrug[0]).exists():
                return Response({'error': '药品不存在'}, status=status.HTTP_400_BAD_REQUEST)

            drug = Drug.objects.get(name=takendrug[0])
            if drug.stock < takendrug[1]:
                return Response({f'error': f'库存{drug}不足,剩余量为{drug.stock}'}, status=status.HTTP_400_BAD_REQUEST)
        for takendrug in takenDrugs:
            drug = Drug.objects.get(name=takendrug[0])
            drug.stock -= takendrug[1]
            drug.save()
            account += drug.price * takendrug[1]
        d.is_taken = True
        d.save()
        return Response({'account': account}, status=status.HTTP_200_OK)
