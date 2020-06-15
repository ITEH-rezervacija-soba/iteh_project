from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator

from .filters import HotelFilter
from .forms import CreateUserForm, CreateReservationForm
from .models import HotelModel, AccommodationModel, HotelImageModel

from datetime import date


@csrf_protect
def login_user(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.info(request, "Username or password is incorrect.")
    return render(request, 'room_reservation/login.html')


def homepage(request):
    return render(request, 'room_reservation/home.html')


@csrf_protect
def register(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get("username")
                messages.success(request, f"Account was created for {user} ")
                return redirect('login')
            else:
                pass1 = form.cleaned_data.get("password1")
                pass2 = form.cleaned_data.get("password2")
                if pass1 != pass2:
                    messages.info(request, "The two password fields didn’t match.")
                else:
                    messages.info(request, "Username is taken.")

        context = {'form': form}
        return render(request, 'room_reservation/register.html', context)


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('homepage')


@login_required(login_url='login')
def user_profile(request):
    return render(request, 'room_reservation/profile.html')


def hotels(request):
    hotels = HotelModel.objects.all()
    my_filter = HotelFilter(request.GET, queryset=hotels)
    hotels = my_filter.qs

    paginator = Paginator(hotels, 3)
    page = request.GET.get('page')
    hotels = paginator.get_page(page)

    context = {"hotels": hotels, "my_filter": my_filter}
    return render(request, 'room_reservation/hotels.html', context)


def hotel_page(request, pk):
    form = CreateReservationForm()
    hotel = HotelModel.objects.get(id=pk)
    images = HotelImageModel.objects.filter(hotel=pk)
    rooms = AccommodationModel.objects.filter(hotel=pk)
    if request.method == 'POST':
        form = CreateReservationForm(request.POST, initial={"user": request.user, "accommodation": pk,
                                                            "reservation_date": date.today(), })
        if form.is_valid():
            form.save()
            return redirect('room_reservation/home.html')
    context = {"form": form, "hotel": hotel, "images": images, "rooms": rooms}
    return render(request, 'room_reservation/hotel_page.html', context)
