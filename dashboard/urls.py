from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.camps_map, name="camps_map"),
    url(r'^camps/', views.camps_geojson, name="camps_geojson"),
    url(r'^addHazard/?', views.add_hazard_area, name="add_hazard_area"),
    url(r'^hazards/', views.hazards_geojson, name="hazards_geojson"),
]