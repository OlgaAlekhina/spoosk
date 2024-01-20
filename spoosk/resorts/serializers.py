from rest_framework import serializers
from .models import SkiResort, SkiPass, ResortImage, SkiReview, ReviewImage


# serializer for SkiPass model
class SkipassSerializer(serializers.ModelSerializer):

    class Meta:
        model = SkiPass
        fields = ('mob_type', 'price')


# serializer for ResortImage model
class ResortImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResortImage
        fields = ('title', 'image')


# serializer for ReviewImage model
class ReviewImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewImage
        fields = ('id', 'image')
        extra_kwargs = {
            'id': {'read_only': True}
        }


# serializer for SkiReview model
class SkireviewSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.first_name')
    author_lastname = serializers.ReadOnlyField(source='author.last_name')
    resort_name = serializers.ReadOnlyField(source='resort.name')
    resort_region = serializers.ReadOnlyField(source='resort.region')
    images = ReviewImageSerializer(source='review_images', many=True, required=False, help_text="list of review's images")

    class Meta:
        model = SkiReview
        fields = ('id', 'resort', 'resort_name', 'resort_region', 'author_name', 'author_lastname', 'text', 'rating', 'add_at', 'images', 'approved')
        extra_kwargs = {
            'approved': {'read_only': True}
        }

    def create(self, validated_data):
        resort = validated_data['resort']
        author = self.context['request'].user
        text = validated_data['text']
        rating = validated_data['rating']
        images = self.context['request'].FILES.getlist('images')
        images_list = list(images)
        review = SkiReview(resort=resort, author=author, text=text, rating=rating)
        review.save()
        for index, image in enumerate(images_list):
            im = ReviewImage(review=review, image=image)
            im.save()
            if index == 9:
                break
        return review


# serializer for SkiReview update action
class SkireviewUpdateSerializer(serializers.ModelSerializer):
    deleted_images = serializers.ListField(child=serializers.IntegerField(), allow_empty=True, max_length=10, required=False, help_text="list of id (integer) of review's images deleted by user")
    images = ReviewImageSerializer(source='review_images', many=True, required=False, help_text="list of review's images")
    rating = serializers.IntegerField(required=False, min_value=1, max_value=5)

    class Meta:
        model = SkiReview
        fields = ('text', 'rating', 'deleted_images', 'images')


# serializer for SkiResort model for retrieve action
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
    rating = serializers.ReadOnlyField(source='resort_rating', help_text="average rating of the resort")
    number_reviews = serializers.ReadOnlyField(source='reviews_count', help_text="number of reviews for the resort")
    images = ResortImageSerializer(source='resort_images', many=True, help_text="list of resort's additional images")

    class Meta:
        model = SkiResort
        fields = '__all__'

# serializer for SkiResort model for list method
class ResortSerializer(serializers.ModelSerializer):
    trail_length = serializers.ReadOnlyField(source='total_length_calculation', help_text="summarized length of all resort's trails [km]")
    height_difference = serializers.ReadOnlyField(source='max_height_difference', help_text="resort's height difference [m]")
    skipass = serializers.ReadOnlyField(source='skipass_min', help_text="minimal price of skipass")
    trail_number = serializers.ReadOnlyField(source='trail_number_count', help_text="number of all resort's trails")
    rating = serializers.ReadOnlyField(source='resort_rating', help_text="average rating of the resort")
    number_reviews = serializers.ReadOnlyField(source='reviews_count', help_text="number of reviews for the resort")

    class Meta:
        model = SkiResort
        fields = ['id_resort', 'name', 'region', 'rating', 'number_reviews', 'image', 'trail_length', 'height_difference', 'skipass', 'trail_number']


