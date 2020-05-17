from django.contrib import admin
from .models import HotelModel, AccommodationModel, AccommodationImageModel, ReservationModel

# Register your models here.

admin.site.register(HotelModel)
admin.site.register(AccommodationModel)
admin.site.register(AccommodationImageModel)
admin.site.register(ReservationModel)