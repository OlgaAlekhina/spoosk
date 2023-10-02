from rest_framework import serializers
from .models import SkiResort

class SkiResortSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkiResort
        fields = '__all__'