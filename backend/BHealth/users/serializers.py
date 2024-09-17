from rest_framework import serializers

from users.models import User, Diagnosis


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'introduction', 'create_time',
                  'update_time', 'workSchedule', 'category']


class DiagnosisSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(source='doctor.username')

    class Meta:
        model = Diagnosis
        fields = ['id', 'doctor', 'content', 'create_time', 'update_time', 'is_delete', ]


class UserSerializer(serializers.ModelSerializer):
    diagnosis = DiagnosisSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'introduction', 'create_time',
                  'update_time', 'diagnosis', 'type']
