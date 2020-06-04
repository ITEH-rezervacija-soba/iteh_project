import django_filters
from .models import HotelModel
from django_filters import DateFilter, CharFilter


class HotelFilter(django_filters.FilterSet):
    city_name = CharFilter(field_name='city_name', lookup_expr='icontains')
    hotel_name = CharFilter(field_name='hotel_name', lookup_expr='icontains')
    address = CharFilter(field_name='address', lookup_expr='icontains')

    class Meta:
        model = HotelModel
        fields = "__all__"
        exclude = ['hotel_image', 'hotel_description']


