from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import RedirectView

from . import views
from .views import login_user, homepage, register, logout_user, user_profile, hotels, hotel_page, create_reservation, update_reservation, delete_reservation


urlpatterns = [
    path('login/', login_user, name='login'),
    path('', RedirectView.as_view(url='homepage/')),
    path('homepage/', homepage, name='homepage'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
    path('profile/', user_profile, name='profile'),
    path('hotels/', hotels, name='hotels'),
    path('hotels/<int:pk>/', hotel_page, name="hotel_page"),
    path('create_reservation/<int:pk>/', create_reservation, name="create_reservation"),
    path('update_reservation/<int:pk>/', update_reservation, name="update_reservation"),
    path('delete_reservation/<int:pk>/', delete_reservation, name="delete_reservation"),
    path('pdf_view/<int:pk>', views.view_as_pdf, name="view_as_pdf"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)