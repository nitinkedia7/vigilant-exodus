import json

from django.contrib.gis.geos import GEOSGeometry, Polygon
from django.core.serializers import serialize
from django.conf import settings
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Camp, Hazard, Person
import json

def camps_geojson(request):
    """
    Retrieves properties given the querystring params, and 
    returns them as GeoJSON.
    """
    ne = request.GET["ne"].split(",")
    sw = request.GET["sw"].split(",")
    lookup = {
        "point__contained": Polygon.from_bbox((sw[1], sw[0], ne[1], ne[0])),
    }
    properties = Camp.objects.filter(**lookup)
    json = serialize("geojson", properties, geometry_field="point")

    return HttpResponse(json, content_type="application/json")

def hazards_geojson(request):
    """
    Retrieves properties given the querystring params, and 
    returns them as GeoJSON.
    """
    ne = request.GET["ne"].split(",")
    sw = request.GET["sw"].split(",")
    lookup = {
        "point__contained": Polygon.from_bbox((sw[1], sw[0], ne[1], ne[0])),
    }
    properties = Hazard.objects.filter(**lookup)
    json = serialize("geojson", properties, geometry_field="point")

    return HttpResponse(json, content_type="application/json")

def people_geojson(request):
    """
    Retrieves properties given the querystring params, and 
    returns them as GeoJSON.
    """
    ne = request.GET["ne"].split(",")
    sw = request.GET["sw"].split(",")
    lookup = {
        "point__contained": Polygon.from_bbox((sw[1], sw[0], ne[1], ne[0])),
    }
    people = Person.objects.filter(**lookup)
    json = serialize("geojson", people, geometry_field="point")

    return HttpResponse(json, content_type="application/json")

@csrf_exempt
def add_hazard_area(request):
    # Get the post variables
    latLng = json.loads(request.body.decode('utf-8'))
    # Create the game object
    try:
        hazard = Hazard.objects.create()
        hazard.set_hazard_location(latlng = latLng)
        hazard.save()
        # Setting output
        response = {
            'status': 200,
            'message': 'Game saved'
        }
        print('Saved hazard location @' + latLng)
    except Exception as e:
        print(e)
        # Something went wrong
        response = {
            'status': 0,
            'message': 'Something went wrong - ' +str(e) 
        }

    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def add_rescue_area(request):
    # Get the post variables
    latLng = json.loads(request.body.decode('utf-8'))
    # Create the game object
    try:
        person = Person.objects.create(name="Robin Hood")
        person.set_location(latlng = latLng)
        person.save()
        # Setting output
        response = {
            'status': 200,
            'message': 'Game saved'
        }
        print('done')
    except Exception as e:
        print(e)
        # Something went wrong
        response = {
            'status': 0,
            'message': 'Something went wrong - ' +str(e) 
        }

    return HttpResponse(json.dumps(response), content_type="application/json")

def camps_map(request):
    """
    Index page for the app, with map + form for filtering 
    properties.
    """
    # Get the center of all properties, for centering the map.
    if False:
    # if Camp.objects.exists():
        cursor = connection.cursor()
        cursor.execute("SELECT ST_AsText(st_centroid(st_union(point))) FROM dashboard_camp")
        print(cursor)
        center = dict(zip(("lng", "lat"), GEOSGeometry(cursor.fetchone()[0]).get_coords()))
    else:
        # Default, when no properties exist.
        center = {"lat":37.782551, "lng": -122.445368}
        # center = {"lat": -33.864869, "lng": 151.1959212}

    context = {
        "center": json.dumps(center),
        "title": "Vigilant Exodus",
        "api_key": settings.GOOGLE_MAPS_API_WEB_KEY,
        "distance_range": (1, 21),
    }

    return render(request, "map.html", context)
    