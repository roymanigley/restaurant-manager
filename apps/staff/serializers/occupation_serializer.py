from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.core.models import Occupation


class OccupationSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        self._validate_start_end(
            validated_data['start'],
            validated_data.get('end')
        )
        return super().create(validated_data)

    def update(self, instance: Occupation, validated_data):
        start = validated_data.get('start')
        end = validated_data.get('end')
        if start is None:
            start = instance.start
        if end is None:
            end = instance.end
        self._validate_start_end(
            start,
            end
        )
        return super().update(instance, validated_data)

    @staticmethod
    def _validate_start_end(start: datetime, end: datetime) -> None:
        if end is None or start < end:
            return
        raise ValidationError('the end date is not bigger than the start date')

    class Meta:
        model = Occupation
        fields = '__all__'
