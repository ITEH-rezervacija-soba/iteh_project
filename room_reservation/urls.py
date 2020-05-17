from django.urls import path, include
from django.views.generic import RedirectView

from .views import login_user, homepage, register, logout_user, user_profile, hotels

urlpatterns = [
    path('login/', login_user, name='login'),
    path('', RedirectView.as_view(url='homepage/')),
    path('homepage/', homepage, name='homepage'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
    path('profile/', user_profile, name='profile'),
    path('hotels/', hotels, name='hotels')
]
