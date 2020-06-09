from django.contrib import admin
from .models import HotelModel, AccommodationModel, ReservationModel, HotelImageModel

# Register your models here.

admin.site.register(HotelModel)
admin.site.register(AccommodationModel)
admin.site.register(ReservationModel)
admin.site.register(HotelImageModel)
