from datetime import datetime

from rest_framework import serializers

from users.models import User, Diagnosis, WorkSchedule, Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    # 返回医生与患者的id而不是用户名
    user = serializers.IntegerField(source='user.id')
    doctor = serializers.IntegerField(source='doctor.id')

    class Meta:
        model = Appointment
        fields = '__all__'


class WorkScheduleSerializer(serializers.ModelSerializer):
    doctor = serializers.IntegerField(source='doctor.id')

    class Meta:
        model = WorkSchedule
        fields = ['id', 'from_time', 'end_time', 'num', 'doctor']


class DoctorSerializer(serializers.ModelSerializer):
    workSchedule = serializers.SerializerMethodField()
    appointment = serializers.SerializerMethodField()

    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['password', 'is_delete', 'is_staff', 'groups', 'user_permissions', 'last_login', ]

    def get_workSchedule(self, obj):
        nowTime = datetime.now().strftime("%Y-%m-%d %H:%M")
        workSchedule = WorkSchedule.objects.filter(doctor=obj).filter(from_time__gte=nowTime)
        serializer = WorkScheduleSerializer(workSchedule, many=True)
        return serializer.data

    def get_appointment(self, obj):
        # nowTime = datetime.now()
        now_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        appointment = Appointment.objects.filter(doctor=obj).filter(from_time__gte=now_time)
        serializer = AppointmentSerializer(appointment, many=True)
        return serializer.data


class DiagnosisSerializer(serializers.ModelSerializer):
    doctor = serializers.IntegerField(source='doctor.id')
    patient = serializers.IntegerField(source='patient.id')

    class Meta:
        model = Diagnosis
        fields = ['id', 'doctor', 'patient', 'content', 'create_time', 'update_time', 'is_delete', ]


class UserSerializer(serializers.ModelSerializer):
    diagnosis = serializers.SerializerMethodField()
    appointment = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ['password', 'is_delete', 'is_staff', 'groups', 'user_permissions', 'last_login', ]

    def get_appointment(self, obj):
        appointment_ids = [app.id for app in Appointment.objects.filter(user=obj).order_by('-create_time')]
        return appointment_ids

    def get_diagnosis(self, obj):
        diagnosis_ids = [diag.id for diag in Diagnosis.objects.filter(patient=obj).order_by('-create_time')]
        return diagnosis_ids
