from datetime import datetime

from rest_framework import serializers

from users.models import User, Diagnosis, WorkSchedule, Appointment


class WorkScheduleSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(source='doctor.username')

    class Meta:
        model = WorkSchedule
        fields = ['id', 'from_time', 'end_time', 'num', 'doctor']


class DoctorSerializer(serializers.ModelSerializer):
    workSchedule = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'introduction', 'create_time',
                  'update_time', 'category', 'workSchedule']

    def get_workSchedule(self, obj):
        nowTime = datetime.now().strftime("%Y-%m-%d %H:%M")
        workSchedule = WorkSchedule.objects.filter(doctor=obj).filter(from_time__gte=nowTime)
        serializer = WorkScheduleSerializer(workSchedule, many=True)
        return serializer.data


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


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(source='doctor.username')
    user = serializers.CharField(source='user.username')

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'user', 'content', 'create_time',
                  'update_time', 'time', 'is_delete', ]
