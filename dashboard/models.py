from django.db import models
from django.conf import settings
from django.contrib.gis.db import models as geomodels
from django.contrib.gis.geos import GEOSGeometry
from geopy.distance import distance
from googlemaps import Client

# Create your models here.
class Disaster(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()

class Camp(geomodels.Model):

    class Meta:
        verbose_name_plural = "Relief Camps"

    address = geomodels.CharField(max_length=256)
    description = geomodels.TextField(null=True, blank=True, default="We provide food, shelter and protection. All are welcome.")
    disaster = models.ForeignKey(Disaster, null=True, blank=True, on_delete=models.PROTECT)
    capacity = geomodels.IntegerField(null=True, default=1000)
    food = geomodels.IntegerField(null=True, default=1000)
    water = geomodels.IntegerField(null=True, default=1000)
    medicine = geomodels.IntegerField(null=True, default=1000)
    place_id = geomodels.CharField(max_length=256, unique=True)
    point = geomodels.PointField(srid=4326, null=True, unique=True)

    def __str__(self):
        return self.address
        
    def set_google_maps_fields(self, latlng=None):
        """
        Uses the Google Maps API to set:
          - geocoded latlng
        """
        client = Client(key=settings.GOOGLE_MAPS_API_SERVER_KEY)
        if not latlng:
            data = client.geocode(self.address)
            if not data:
                raise Exception("Unable to resolve the address: '%s'" % address)
            latlng = data[0]["geometry"]["location"]
        self.point = GEOSGeometry("POINT(%(lng)s %(lat)s)" % latlng)

class Hazard(geomodels.Model):
    disaster = models.ForeignKey(Disaster, null=True, blank=True, on_delete=models.PROTECT)
    point = geomodels.PointField(srid=4326, null=True)
    description = geomodels.TextField(null=True, default="Compromised area, keep distance")
    weight = geomodels.IntegerField(default=1)

    def set_hazard_location(self, latlng):
        if latlng:
            self.point = GEOSGeometry("POINT(%(lng)s %(lat)s)" % latlng)
        else:
            raise Exception("latlng is NULL")

class Person(geomodels.Model):
    name = models.CharField(max_length=45)
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(null=True, max_length=32)
    emergencyName = models.CharField(null=True, max_length=32)
    emergencyPhone = models.CharField(null=True, max_length=32)
    camp = models.ForeignKey(Camp, null=True, blank=True, on_delete=models.PROTECT)
    point = geomodels.PointField(srid=4326, null=True)
 
    def set_location(self, latlng):
        if latlng:
            self.point = GEOSGeometry("POINT(%(lng)s %(lat)s)" % latlng)
        else:
            raise Exception("latlng is NULL")