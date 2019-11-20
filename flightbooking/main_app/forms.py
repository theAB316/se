from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):

	#password = forms.CharField(widget=forms.PasswordInput) 

	class Meta:
		model = User
		fields = ['username', 'email', 'password']

class UserDetailsForm(forms.Form):
	first_name = forms.CharField(label="First Name", max_length=50)
	last_name = forms.CharField(label="Last Name", max_length=50)
	age = forms.IntegerField(label="Age")
	gender = forms.CharField(label="Gender", max_length=1)

	address = forms.CharField(label="Address", max_length=100)
	city = forms.CharField(label="City", max_length=100)
	zipcode = forms.CharField(label="Zip Code", max_length=6)

	departure_time = forms.TimeField(label="Departure Time")
	arrival_time = forms.TimeField(label="Arrival Time")
	
	departure_city= forms.CharField(label="Departure City")
	arrival_city= forms.CharField(label="Arrival City")

	flight_name = forms.CharField(label="Flight Name", max_length=100)

	email = forms.CharField(label="Email ID", max_length=100)

	class Meta:
		fields = ['first_name', 'last_name', 'age']