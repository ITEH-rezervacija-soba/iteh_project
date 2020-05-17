import django
from django.db import models


class HotelModel(models.Model):
    city_name = models.CharField(max_length=255, blank=False)
    hotel_name = models.CharField(max_length=255, blank=False)
    address = models.CharField(max_length=255, blank=False)
    category = models.CharField(max_length=255, blank=False)
    hotel_image = models.ImageField(upload_to=None)


BED_CHOICES = [
    ('1', 'One'),
    ('2', 'Two'),
    ('3', 'Three'),
    ('4', 'Four'),
    ('5', 'Five'),
    ('6', 'Six'),
]


class AccommodationModel(models.Model):
    hotel = models.ForeignKey(HotelModel, null=False, on_delete=models.CASCADE)
    accommodation_name = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    number_of_beds = models.IntegerField(choices=BED_CHOICES)
    balcony = models.BooleanField()
    price_per_night = models.DecimalField(decimal_places=2, max_digits=10)


class AccommodationImageModel(models.Model):
    accommodation = models.ForeignKey(AccommodationModel, null=False, on_delete=models.CASCADE)
    image_name = models.CharField(max_length=255, null=False)
    image = models.ImageField(upload_to=None)


class ReservationModel(models.Model):
    user = models.ForeignKey(django.contrib.auth.get_user_model(), null=True, on_delete=models.CASCADE)
    accommodation = models.ForeignKey(AccommodationModel, null=False, on_delete=models.CASCADE)
    reservation_date = models.DateField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(decimal_places=2, max_digits=10)

