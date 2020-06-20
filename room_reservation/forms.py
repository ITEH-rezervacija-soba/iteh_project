from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, DateField, DateInput
from pylint.checkers.typecheck import _

from .models import ReservationModel


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class CreateReservationForm(ModelForm):

    start_date = DateField(input_formats=["%d.%m.%Y."])
    end_date = DateField(input_formats=["%d.%m.%Y."])

    class Meta:
        model = ReservationModel
        fields = ['accommodation','start_date','end_date']
