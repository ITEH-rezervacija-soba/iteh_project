from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import RedirectView

from .views import login_user, homepage, register, logout_user, user_profile, hotels, hotel_page, create_reservation


urlpatterns = [
    path('login/', login_user, name='login'),
    path('', RedirectView.as_view(url='homepage/')),
    path('homepage/', homepage, name='homepage'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
    path('profile/', user_profile, name='profile'),
    path('hotels/', hotels, name='hotels'),
    path('hotels/<int:pk>/', hotel_page, name="hotel_page"),
    path('create_reservation/', create_reservation, name="create_reservation"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)