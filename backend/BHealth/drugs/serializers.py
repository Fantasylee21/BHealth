from rest_framework import serializers

from drugs.models import Drug


class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ('id', 'name', 'price','stock', 'description', 'create_time', 'update_time', 'is_delete')
