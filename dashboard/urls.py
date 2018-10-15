from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.camps_map, name="camps_map"),
    url(r'^camps/', views.camps_geojson, name="camps_geojson"),
]