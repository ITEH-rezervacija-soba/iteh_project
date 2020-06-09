from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import RedirectView

from .views import api_overview, wish_list, wish_detail, wish_create, wish_update, wish_delete

urlpatterns = [

    path('api/', api_overview, name="api_overview"),
    path('api/wish-list/', wish_list, name="wish_list"),
    path('api/wish-detail/<str:pk>/', wish_detail, name="wish_detail"),
    path('api/wish-create/', wish_create, name="wish_create"),
    path('api/wish-update/<str:pk>', wish_update, name="wish_update"),
    path('api/wish-delete/<str:pk>', wish_delete, name="wish_delete"),
]
