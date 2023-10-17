from rest_framework import serializers
from .models import SkiResort

class SkiResortSerializer(serializers.ModelSerializer):
    trail_length = serializers.ReadOnlyField(source='total_length_calculation', help_text="summarized length of all resort's trails [km]")
    trail_number = serializers.ReadOnlyField(source='trail_number_count', help_text="number of all resort's trails")
    skipass = serializers.ReadOnlyField(source='skipass_min', help_text="minimal price of skipass")

    class Meta:
        model = SkiResort
        fields = '__all__'
