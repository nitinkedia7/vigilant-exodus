import random

from django.conf import settings
from django.core.management.base import BaseCommand
import googlemaps

from dashboard.models import Camp


class Command(BaseCommand):
    """
    Utility for populating the database with random (real) locations.
    """

    def add_arguments(self, parser):
        parser.add_argument("--center", action="store", dest="center", default="37.772544,-122.4228374",
            help="Center of area where locations will be randomly drawn from, eg: --center %(default)s")
        parser.add_argument("--radius", action="store", dest="radius", default=50000, type=int,
            help="Radius from center upto which places will be queried.")
        parser.add_argument("--delete", action="store_true", dest="delete",
            help="Delete existing records before populating.")

    def handle(self, **options):
        client = googlemaps.Client(key=settings.GOOGLE_MAPS_API_SERVER_KEY)
        camps = []
        start_lat, start_lng = map(float, options["center"].split(","))
        step = {"lat": 3.0, "lng": 5.0}
        types = "school,hospital,airport,stadium"
        try:
            latlng = {
                "lat": random.uniform(start_lat + (step["lat"]), start_lat - (step["lat"])),
                "lng": random.uniform(start_lng - (step["lng"]), start_lng + (step["lng"])),
            }
            place_results = client.places_nearby(location=options["center"], radius=options["radius"], type=types)    
            # count = 5
            for result in place_results['results']:
                camp = Camp(place_id = result["place_id"],
                            name = result["name"],
                            address = result["vicinity"])
                camp.set_google_maps_fields(latlng=result["geometry"]["location"])
                camps.append(camp)
                print("Resolved %s" % result["name"])
                # count -= 1
                # if (count == 0):
                    # break
        except Exception as e:
            print("Error: %s" % e)
        
        if options["delete"]:
            print("Deleting %s old camps" % Camp.objects.count())
            Camp.objects.all().delete()
        Camp.objects.bulk_create(camps)
        print("Inserted %s camps" % len(camps))
