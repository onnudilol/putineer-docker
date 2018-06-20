from rest_framework import serializers
from restaurant.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()
    coords = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = '__all__'

    def get_distance(self, obj):
        return f'{obj.distance.km:.2}'

    def get_coords(self, obj):
        coords = obj.coords.coords

        return list(coords)
