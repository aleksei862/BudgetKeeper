from rest_framework import serializers
from finance.models import Operation

class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = '__all__'

    # Валидация: сумма не может быть отрицательной
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Сумма операции должна быть больше нуля.")
        return value