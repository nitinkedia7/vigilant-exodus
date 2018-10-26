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
        parser.add_argument("--num", action="store", dest="num", default=10, type=int,
            help="Number of records to add - note that each record will use Google's reverse "
                 "geocoding API and Places API, counting towards up to 3 requests per record "
                 "against your daily quota.")
        parser.add_argument("--center", action="store", dest="center", default="37.772544,-122.4228374",
            help="Center of area where locations will be randomly drawn from, eg: --center %(default)s")
        parser.add_argument("--delete", action="store_true", dest="delete",
            help="Delete existing records before populating.")

    def handle(self, **options):
        client = googlemaps.Client(key=settings.GOOGLE_MAPS_API_SERVER_KEY)
        properties = []
        start_lat, start_lng = map(float, options["center"].split(","))
        step = {"lat": 2.0, "lng": 4.0}
        seen = set()
        
        for i in range(options["num"] + 1, 1, -1):
            # Random latlng within a boundary that grows out from the center 
            # as iteration occurs.
            latlng = {
                "lat": random.uniform(start_lat + (step["lat"]/i), start_lat - (step["lat"]/i)),
                "lng": random.uniform(start_lng - (step["lng"]/i), start_lng + (step["lng"]/i)),
            }
            try:
                result = client.reverse_geocode(latlng)[0]
                address = result["formatted_address"]
                latlng = result["geometry"]["location"]
            except Exception as e:
                print("Error: %s" % e)
                continue
            # Resolved addresses aren't always postal addresses - they could represent a landmark
            # or area of some sort. Sticking with addresses that begin with a digit works 
            # reasonably well.
            if not address[0].isdigit():
                print("Skipping non-postal address: %s" % address)
                continue
            # Discard duplicates
            if address in seen:
                print("Skipping duplicate address: %s" % address)
                continue
            seen.add(address)
            property = Camp(place_id = result["place_id"],
                        address = result["formatted_address"])
            property.set_google_maps_fields(latlng=latlng)
            # # Set a random value for each of the range fields.
            for field in ("capacity", "food", "medicine", "water"):
                setattr(property, field, random.uniform(200, 1001))
            properties.append(property)
            print("Resolved %s" % address)
        
        if options["delete"]:
            print("Deleting %s old properties" % Camp.objects.count())
            Camp.objects.all().delete()
        Camp.objects.bulk_create(properties)
        print("Inserted %s properties" % len(properties))
