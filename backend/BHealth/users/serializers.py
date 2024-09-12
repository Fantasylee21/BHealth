from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email',  'avatar', 'introduction', 'create_time',
                  'update_time', ]

class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'introduction', 'create_time',
                  'update_time', 'workSchedule',]