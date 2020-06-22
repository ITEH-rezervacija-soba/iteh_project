from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator

from .filters import HotelFilter
from .forms import CreateUserForm, CreateReservationForm
from .models import HotelModel, AccommodationModel, HotelImageModel, ReservationModel

from datetime import date
TIME_FORMAT = '%d.%m.%Y'
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
    # WEB SERVIS ZA KONVERZIJU VALUTA
    url = "https://api.exchangeratesapi.io/latest?symbols=USD,GBP"
    response = requests.get(url)
    data = response.text
    parsed = json.loads(data)

    base = parsed['base']
    currencies = [base] + list(parsed['rates'])
    curr_vals = [1] + list(parsed["rates"].values())

    reservations = ReservationModel.objects.filter(user=request.user)
    for res in reservations:
        hotel = AccommodationModel.objects.get(id=res.accommodation.id).hotel
        res.hotel = HotelModel.objects.get(id=hotel.id)
        if res.start_date > date.today():
            res.status = f'Pending - start date: {res.start_date.strftime("%d.%m.%Y.")}'
        elif res.end_date < date.today():
            res.status = f'Checked out {res.end_date.strftime("%d.%m.%Y.")}'
        else:
            res.status = f'Checked in {res.start_date.strftime("%d.%m.%Y.")}'
    context = {"reservations":reservations, "values": curr_vals,"currencies": currencies}
    return render(request, 'room_reservation/home.html',context)


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

    # WEB SERVIS ZA KONVERZIJU VALUTA
    url = "https://api.exchangeratesapi.io/latest?symbols=USD,GBP"
    response = requests.get(url)
    data = response.text
    parsed = json.loads(data)

    base = parsed['base']
    currencies = [base] + list(parsed['rates'])
    curr_vals = [1] + list(parsed["rates"].values())

    context = {"hotel": hotel, "images": images, "rooms": rooms, "currencies": currencies, "values": curr_vals}
    return render(request, 'room_reservation/hotel_page.html', context)


def create_reservation(request,pk):
    acc = AccommodationModel.objects.get(id = pk)
    obj = ReservationModel(accommodation_id=acc.id)
    form = CreateReservationForm(instance = obj)
    if request.method == "POST":
        form = CreateReservationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if obj.start_date < date.today():
                messages.info(request, "Start date can not be in the past")
                return redirect('create_reservation',pk=pk)
            reservations = ReservationModel.objects.filter(accommodation=obj.accommodation)
            for res in reservations:
                if ((res.start_date >= obj.start_date) & (res.start_date <= obj.end_date)) | ((res.end_date >= obj.start_date) & (res.end_date <= obj.end_date)) | ((res.start_date <= obj.start_date) & (obj.end_date <= res.end_date)):
                    messages.info(request, "Room is already booked for this dates")
                    return redirect('create_reservation',pk=pk)
            obj.user = request.user
            obj.reservation_date = date.today()
            obj.total_price = obj.accommodation.price_per_night * int((obj.end_date - obj.start_date).days)
            if obj.total_price < 0:
                messages.info(request, "Start date has to be before end date!")
                return redirect('create_reservation',pk=pk)
            obj.save()
            return redirect('homepage')
        else:
            messages.info(request, "You have to fill all the fields to make a reservation."
                                   " Date format is DD.MM.YYYY")

    context = {"form": form}
    return render(request, 'room_reservation/reservation.html', context)

def update_reservation(request,pk):

    reservation = ReservationModel.objects.get(id=pk)

    form = CreateReservationForm(instance = reservation,initial={'start_date':reservation.start_date.strftime(TIME_FORMAT),
                                                                 'end_date':reservation.end_date.strftime(TIME_FORMAT)})

    if request.method == "POST":
        form = CreateReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            obj = form.save(commit=False)
            if obj.start_date < date.today():
                messages.info(request, "Start date can not be in the past")
                return redirect('update_reservation',pk = reservation.id)
            if obj.start_date > obj.end_date:
                messages.info(request, "Start date has to be before end date!")
                return redirect('update_reservation',pk = reservation.id)
            reservations = ReservationModel.objects.filter(accommodation=obj.accommodation).exclude(id=pk)
            for res in reservations:
                if ((res.start_date >= obj.start_date) & (res.start_date <= obj.end_date)) | (
                        (res.end_date >= obj.start_date) & (res.end_date <= obj.end_date)) | (
                        (res.start_date <= obj.start_date) & (obj.end_date <= res.end_date)):
                    messages.info(request, "Room is already booked for this dates")
                    return redirect('update_reservation',pk = reservation.id)
            obj.user = request.user
            obj.reservation_date = date.today()
            obj.total_price = obj.accommodation.price_per_night * int((obj.end_date - obj.start_date).days)
            obj.save()
            return redirect('homepage')
        else:
            messages.info(request, "You have to fill all the fields to make a reservation."
                                   " Date format is DD.MM.YYYY.")

    context = {"form":form}
    return render(request, 'room_reservation/reservation.html', context)

def delete_reservation(request,pk):
    reservation = ReservationModel.objects.get(id=pk)
    message = f"Are you sure you want to cancel reservation {reservation}?" if reservation.start_date > date.today() else f"Are you sure you want to remove reservation {reservation} from the list?"
    if request.method == "POST":
        reservation.delete()
        return redirect('homepage')
    context = {"message":message,"reservation":reservation}
    return  render(request, 'room_reservation/delete_reservation.html',context)

def weather(request):

    #Web service za vreme, prikazuje trenunto samo London u json formatu

    data = requests.get("http://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}&units={2}".format('London','1cf038b92a748c3271a76ede2fcd7f0c','metric'))

    data_json = data.json()


    context = {"data":data_json}
    return render(request, 'room_reservation/weather.html', context)


# -izmena,  otkazivanje