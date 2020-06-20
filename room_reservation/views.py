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
import requests, json

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
    hotel = HotelModel.objects.get(id=pk)
    images = HotelImageModel.objects.filter(hotel=pk)
    rooms = AccommodationModel.objects.filter(hotel=pk)

    #WEB SERVIS ZA KONVERZIJU VALUTA
    url = "https://api.exchangeratesapi.io/latest?symbols=USD,GBP"
    response = requests.get(url)
    data = response.text
    parsed = json.loads(data)

    base = parsed['base']
    other_currencies = list(parsed['rates'])
    curr_vals = list(parsed["rates"].values())
    form_list = zip(other_currencies, curr_vals)
    context = {"hotel": hotel, "images": images, "rooms": rooms, "base": base, "form_list": form_list}
    return render(request, 'room_reservation/hotel_page.html', context)


def create_reservation(request):


    form = CreateReservationForm()
    if request.method == "POST":
        form = CreateReservationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.reservation_date = date.today()
            obj.total_price = obj.accommodation.price_per_night * int((obj.end_date - obj.start_date).days)
            obj.save()
            return redirect('homepage')
        else:
            messages.info(request, "You have to fill all the fields to make a reservation."
                                   " Date format is DD.MM.YYYY.")

    context = {"form": form}
    return render(request, 'room_reservation/create_reservation.html', context)


def weather(request):

    # WEB SERVIS ZA PRETRAGU MESTA DESAVANJA

    data = requests.get("http://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}&units={2}".format('London','1cf038b92a748c3271a76ede2fcd7f0c','metric'))

    data_json = data.json()


    context = {"data":data_json}
    return render(request, 'room_reservation/weather.html', context)

# -ogranicenja za rezervacije
# -prikaz rezervacije
# -izmena,  otkazivanje