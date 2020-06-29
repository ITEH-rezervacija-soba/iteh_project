import urllib

import requests, json
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

from .filters import HotelFilter, ReservationFilter, AccomodationFilter
from .forms import CreateUserForm, CreateReservationForm
from .models import HotelModel, AccommodationModel, HotelImageModel, ReservationModel

from datetime import date

TIME_FORMAT = '%d.%m.%Y'


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
    key = 'LQBJ8397PZR8L3UK'
    london_data = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}&units={2}".format('London',
                                                                                          '1cf038b92a748c3271a76ede2fcd7f0c',
                                                                                          'metric'))

    london_json = london_data.json()
    london_temp = london_json['main']['temp']
    london_temp_min = london_json['main']['temp_min']
    london_temp_max = london_json['main']['temp_max']
    london_humidity = london_json['main']['humidity']
    london = {'temp': london_temp, 'temp_min': london_temp_min, 'temp_max': london_temp_max,
              'humidity': london_humidity}

    urllib.request.urlopen(f'https://api.thingspeak.com/update?api_key={key}&field1={london_temp}')

    belgrade_data = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}&units={2}".format('Belgrade',
                                                                                          '1cf038b92a748c3271a76ede2fcd7f0c',
                                                                                          'metric'))

    belgrade_json = belgrade_data.json()
    belgrade_temp = belgrade_json['main']['temp']
    belgrade_temp_min = belgrade_json['main']['temp_min']
    belgrade_temp_max = belgrade_json['main']['temp_max']
    belgrade_humidity = belgrade_json['main']['humidity']
    belgrade = {'temp': belgrade_temp, 'temp_min': belgrade_temp_min, 'temp_max': belgrade_temp_max,
                'humidity': belgrade_humidity}
    urllib.request.urlopen(f'https://api.thingspeak.com/update?api_key={key}&field2={belgrade_temp}')

    paris_data = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}&units={2}".format('Paris',
                                                                                          '1cf038b92a748c3271a76ede2fcd7f0c',
                                                                                          'metric'))

    paris_json = paris_data.json()
    paris_temp = paris_json['main']['temp']
    paris_temp_min = paris_json['main']['temp_min']
    paris_temp_max = paris_json['main']['temp_max']
    paris_humidity = paris_json['main']['humidity']
    paris = {'temp': paris_temp, 'temp_min': paris_temp_min, 'temp_max': paris_temp_max, 'humidity': paris_humidity}
    urllib.request.urlopen(f'https://api.thingspeak.com/update?api_key={key}&field3={paris_temp}')

    context = {'london': london, 'belgrade': belgrade, 'paris': paris}
    return render(request, 'room_reservation/home.html', context)


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
    # WEB SERVIS ZA KONVERZIJU VALUTA
    url = "https://api.exchangeratesapi.io/latest?symbols=USD,GBP"
    response = requests.get(url)
    data = response.text
    parsed = json.loads(data)

    base = parsed['base']
    currencies = [base] + list(parsed['rates'])
    curr_vals = [1] + list(parsed["rates"].values())

    reservations = ReservationModel.objects.filter(user=request.user)
    my_filter = ReservationFilter(request.GET, queryset=reservations)
    reservations = my_filter.qs
    for res in reservations:
        hotel = AccommodationModel.objects.get(id=res.accommodation.id).hotel
        res.hotel = HotelModel.objects.get(id=hotel.id)
        if res.start_date > date.today():
            res.status = f'Pending - start date: {res.start_date.strftime("%d.%m.%Y.")}'
        elif res.end_date < date.today():
            res.status = f'Checked out {res.end_date.strftime("%d.%m.%Y.")}'
        else:
            res.status = f'Checked in {res.start_date.strftime("%d.%m.%Y.")}'
    current_user = request.user
    context = {"reservations": reservations, "values": curr_vals, "currencies": currencies,
               "current_user": current_user, "my_filter": my_filter}
    return render(request, 'room_reservation/profile.html', context)


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
    my_filter = AccomodationFilter(request.GET, queryset=rooms)
    rooms = my_filter.qs

    # WEB SERVIS ZA KONVERZIJU VALUTA
    url = "https://api.exchangeratesapi.io/latest?symbols=USD,GBP"
    response = requests.get(url)
    data = response.text
    parsed = json.loads(data)

    base = parsed['base']
    currencies = [base] + list(parsed['rates'])
    curr_vals = [1] + list(parsed["rates"].values())

    context = {"hotel": hotel, "images": images, "rooms": rooms, "currencies": currencies, "values": curr_vals,
               "my_filter": my_filter}
    return render(request, 'room_reservation/hotel_page.html', context)


@login_required(login_url='login')
def create_reservation(request, pk):
    acc = AccommodationModel.objects.get(id=pk)
    hotel = HotelModel.objects.get(id=acc.hotel.id)
    obj = ReservationModel(accommodation_id=acc.id)
    form = CreateReservationForm(instance=obj)
    if request.method == "POST":
        form = CreateReservationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if obj.start_date < date.today():
                messages.info(request, "Start date can not be in the past")
                return redirect('create_reservation', pk=pk)
            reservations = ReservationModel.objects.filter(accommodation=obj.accommodation)
            for res in reservations:
                if ((res.start_date >= obj.start_date) & (res.start_date <= obj.end_date)) | (
                        (res.end_date >= obj.start_date) & (res.end_date <= obj.end_date)) | (
                        (res.start_date <= obj.start_date) & (obj.end_date <= res.end_date)):
                    messages.info(request, "Room is already booked for this dates")
                    return redirect('create_reservation', pk=pk)
            obj.user = request.user
            obj.reservation_date = date.today()
            obj.total_price = obj.accommodation.price_per_night * int((obj.end_date - obj.start_date).days)
            if obj.total_price < 0:
                messages.info(request, "Start date has to be before end date!")
                return redirect('create_reservation', pk=pk)
            obj.save()
            return redirect('profile')
        else:
            messages.info(request, "You have to fill all the fields to make a reservation."
                                   " Date format is DD.MM.YYYY")

    context = {"form": form, "acc": acc, "hotel": hotel}
    return render(request, 'room_reservation/reservation.html', context)


@login_required(login_url='login')
def update_reservation(request, pk):
    reservation = ReservationModel.objects.get(id=pk)
    acc = AccommodationModel.objects.get(id=reservation.accommodation.id)
    hotel = HotelModel.objects.get(id=acc.hotel.id)
    obj = ReservationModel(accommodation_id=acc.id)
    form = CreateReservationForm(instance=reservation,
                                 initial={'start_date': reservation.start_date.strftime(TIME_FORMAT),
                                          'end_date': reservation.end_date.strftime(TIME_FORMAT)})

    if request.method == "POST":
        form = CreateReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            obj = form.save(commit=False)
            if obj.start_date < date.today():
                messages.info(request, "Start date can not be in the past")
                return redirect('update_reservation', pk=reservation.id)
            if obj.start_date > obj.end_date:
                messages.info(request, "Start date has to be before end date!")
                return redirect('update_reservation', pk=reservation.id)
            reservations = ReservationModel.objects.filter(accommodation=obj.accommodation).exclude(id=pk)
            for res in reservations:
                if ((res.start_date >= obj.start_date) & (res.start_date <= obj.end_date)) | (
                        (res.end_date >= obj.start_date) & (res.end_date <= obj.end_date)) | (
                        (res.start_date <= obj.start_date) & (obj.end_date <= res.end_date)):
                    messages.info(request, "Room is already booked for this dates")
                    return redirect('update_reservation', pk=reservation.id)
            obj.user = request.user
            obj.reservation_date = date.today()
            obj.total_price = obj.accommodation.price_per_night * int((obj.end_date - obj.start_date).days)
            obj.save()
            return redirect('homepage')
        else:
            messages.info(request, "You have to fill all the fields to make a reservation."
                                   " Date format is DD.MM.YYYY.")

    context = {"form": form, "hotel": hotel}
    return render(request, 'room_reservation/reservation.html', context)


@login_required(login_url='login')
def delete_reservation(request, pk):
    reservation = ReservationModel.objects.get(id=pk)
    acc = AccommodationModel.objects.get(id=reservation.accommodation.id)
    hotel = HotelModel.objects.get(id=acc.hotel.id)
    message = f"Are you sure you want to cancel reservation {reservation}?" if reservation.start_date > date.today() else f"Are you sure you want to remove reservation {reservation} from the list?"
    if request.method == "POST":
        reservation.delete()
        return redirect('homepage')
    context = {"message": message, "reservation": reservation, "hotel":hotel}
    return render(request, 'room_reservation/delete_reservation.html', context)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


@login_required(login_url='login')
def view_as_pdf(request, pk):
    current_user = request.user
    reservation = ReservationModel.objects.get(id=pk)
    accommodation = AccommodationModel.objects.get(id=reservation.accommodation.id)
    hotel = HotelModel.objects.get(id=accommodation.hotel.id)
    total_days = reservation.end_date - reservation.start_date
    context = {"user": current_user, "reservation": reservation, "accommodation": accommodation, "hotel": hotel,
               "total_days": total_days}
    pdf = render_to_pdf('room_reservation/pdf_template.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
