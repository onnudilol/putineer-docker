from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.core.management import call_command
from geopy.geocoders import Nominatim
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from restaurant.models import Restaurant
from restaurant.forms import VerificationForm
from restaurant.serializers import RestaurantSerializer


def get_current_address(coords):
    geolocator = Nominatim()
    current_location = geolocator.reverse(coords)
    current_address = current_location.raw['address']['city']

    return current_address


@api_view(['GET'])
def nearby_restaurants(request):
    data = request.query_params

    pnt = Point(float(data['lat']), float(data['lon']))

    qs = Restaurant.objects.filter(coords__distance_lte=(pnt, D(km=10))) \
        .annotate(distance=Distance('coords', pnt)) \
        .order_by('distance')

    # try scraping yelp api for restaurants at request coords, modifies the db on a GET request but whatever
    if len(qs) == 0:
        call_command('scrape_yelp', 'poutine', coord=f'{data["lat"]}, {data["lon"]}')
        qs = Restaurant.objects.filter(coords__distance_lte=(pnt, D(km=10))) \
            .annotate(distance=Distance('coords', pnt)) \
            .order_by('distance')

    serializer = RestaurantSerializer(qs, many=True)
    response = list(serializer.data)
    current_address = {'current_address': get_current_address(f'{data["lat"]}, {data["lon"]}')}
    response.append(current_address)

    return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def verify_restaurant(request):
    data = request.data
    form = VerificationForm(data)

    if form.is_valid():
        form.save()
        return Response(status.HTTP_201_CREATED)

    else:
        return Response(status.HTTP_400_BAD_REQUEST)
