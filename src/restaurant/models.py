from django.contrib.gis.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=280)
    yelp_id = models.CharField(max_length=30, unique=True)
    yelp_url = models.URLField(max_length=300)
    image_url = models.URLField(max_length=300)
    verified = models.BooleanField(default=False)
    address = models.CharField(max_length=300)
    coords = models.PointField()


class VerificationRequest(models.Model):
    restaurant = models.ForeignKey(Restaurant, null=True, blank=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
