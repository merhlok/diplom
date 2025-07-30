from rest_framework import serializers
from .models import Post,Comment,ImageModel
from geopy.geocoders import Nominatim



class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model=ImageModel
        fields = ['image']


class LocationSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        geolocator = Nominatim(user_agent="social_network")
        location = geolocator.reverse((instance.latitude, instance.longitude))
        return location.address

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializers(serializers.ModelSerializer):
    comment= CommentSerializers(many =True,read_only=True)
    image= ImageSerializers(many =True,read_only=True,source ='image')
    like_count = serializers.IntegerField(read_only=True)
    location_name = serializers.CharField(read_only=True)
    class Meta:
        model = Post
        fields = [
            'id', 'user', 'text', 'created_at', 'image', 
            'comment', 'like_count', 'location_query',
            'latitude', 'longitude', 'location_name'
        ]
        extra_kwargs = {
            'location_query': {'write_only': True},
            'latitude': {'read_only': True},
            'longitude': {'read_only': True},
        }

