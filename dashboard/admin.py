from django.contrib import admin
from .models import Disaster, Camp, Hazard, Person

# Register your models here

admin.site.register(Camp)
admin.site.register(Disaster)
admin.site.register(Person)
admin.site.register(Hazard)
