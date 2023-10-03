from rest_framework import serializers
from .models import SkiResort

class SkiResortSerializer(serializers.ModelSerializer):
    trail_length = serializers.ReadOnlyField(source='total_length_calculation')

    class Meta:
        model = SkiResort
        fields = '__all__'