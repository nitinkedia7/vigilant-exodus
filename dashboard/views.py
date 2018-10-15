import json

from django.contrib.gis.geos import GEOSGeometry, Polygon
from django.core.serializers import serialize
from django.conf import settings
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render

from .models import Camp

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
        center = {"lat": -33.864869, "lng": 151.1959212}

    context = {
        "center": json.dumps(center),
        "title": "Camp Finder",
        "api_key": settings.GOOGLE_MAPS_API_WEB_KEY,
        "distance_range": (1, 21),
    }

    return render(request, "map.html", context)
    