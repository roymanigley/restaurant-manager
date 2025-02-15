from rest_framework import serializers

from apps.core.models import Table


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

class TableAvailabilitySerializer(serializers.Serializer):
    date_time = serializers.DateTimeField(write_only=True)
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    seats = serializers.IntegerField(read_only=True)