from rest_framework import serializers
from .models import SkiResort, SkiPass


# serializer for SkiPass model
class SkipassSerializer(serializers.ModelSerializer):

    class Meta:
        model = SkiPass
        fields = ('name', 'type', 'price')


# serializer for SkiResort model
class SkiResortSerializer(serializers.ModelSerializer):
    trail_length = serializers.ReadOnlyField(source='total_length_calculation', help_text="summarized length of all resort's trails [km]")
    trail_number = serializers.ReadOnlyField(source='trail_number_count', help_text="number of all resort's trails")
    skipass = serializers.ReadOnlyField(source='skipass_min', help_text="minimal price of skipass")
    height_difference = serializers.ReadOnlyField(source='max_height_difference', help_text="resort's height difference [m]")
    green_trails = serializers.ReadOnlyField(source='number_green_trails', help_text="number of green trails of resort")
    blue_trails = serializers.ReadOnlyField(source='number_blue_trails', help_text="number of blue trails of resort")
    red_trails = serializers.ReadOnlyField(source='number_red_trails', help_text="number of red trails of resort")
    black_trails = serializers.ReadOnlyField(source='number_black_trails', help_text="number of black trails of resort")
    gondola_skilift = serializers.ReadOnlyField(source='number_gondola', help_text="number of gondola skilifts of resort")
    armchair_skilift = serializers.ReadOnlyField(source='number_armchair', help_text="number of armchair skilifts of resort")
    travelators_skilift = serializers.ReadOnlyField(source='number_travelators', help_text="number of travelator skilifts of resort")
    bugelny_skilift = serializers.ReadOnlyField(source='number_bugelny', help_text="number of bugelny skilifts of resort")
    skipasses = SkipassSerializer(source='resorts', many=True, help_text="list of resort's skipasses")

    class Meta:
        model = SkiResort
        fields = '__all__'
