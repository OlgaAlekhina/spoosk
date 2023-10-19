from rest_framework import serializers
from .models import SkiResort

class SkiResortSerializer(serializers.ModelSerializer):
    trail_length = serializers.ReadOnlyField(source='total_length_calculation')
    trail_number = serializers.ReadOnlyField(source='trail_number_count')
    skipass = serializers.ReadOnlyField(source='skipass_min')

    class Meta:
        model = SkiResort
        fields = '__all__'