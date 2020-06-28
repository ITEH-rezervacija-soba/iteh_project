import django_filters

from .models import HotelModel, ReservationModel, AccommodationModel
from django_filters import DateFilter, CharFilter, NumberFilter


class HotelFilter(django_filters.FilterSet):
    city_name = CharFilter(field_name='city_name', lookup_expr='icontains')
    hotel_name = CharFilter(field_name='hotel_name', lookup_expr='icontains')
    address = CharFilter(field_name='address', lookup_expr='icontains')

    class Meta:
        model = HotelModel
        fields = "__all__"
        exclude = ['hotel_image', 'hotel_description']


class ReservationFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='start_date', lookup_expr='gte')
    end_date = DateFilter(field_name='end_date', lookup_expr='lte')
    total_price_1 = NumberFilter(field_name='total_price', lookup_expr='gte')
    total_price_2 = NumberFilter(field_name='total_price', lookup_expr='lte')

    class Meta:
        model = ReservationModel
        fields = "__all__"
        exclude = ['user', 'reservation_date', 'total_price']


class AccomodationFilter(django_filters.FilterSet):
    price_1 = NumberFilter(field_name='price_per_night', lookup_expr='gte')
    price_2 = NumberFilter(field_name='price_per_night', lookup_expr='lte')

    class Meta:
        model = AccommodationModel
        fields = "__all__"
        exclude = ['hotel', 'description', 'accommodation_name', 'price_per_night']

