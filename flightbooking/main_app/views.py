# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from django.views import generic
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
	
from .models import User, Flight

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm



# Create your views here.
class UserFormView(TemplateView):
	form_class = UserForm
	template_name = 'main_app/register.html'
	
	#display blank form for new login
	def get(self, request):
		if "username" in request.session:
			del request.session["username"]
			logout(request)

		form = self.form_class(None)
		return render(request, self.template_name, {'form':form})

	#after submit
	def post(self, request):
		form = UserForm(data=request.POST)

		#print(type(form),form, "123\n\n\n\n")
		un = request.POST.get("username", " ")
		print(request.POST)

		if(form.is_valid()):
			user = form.save(commit=False)#not saved to db yet
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			print("\n\n\n\n",username, password)
			user.set_password(password) #set password 

			user.save()

			#return user if correct

			user = authenticate(username=username, password=password)
			
			if user is not None:
				
				if user.is_active:
					login(request, user)
					#refer user as request.user
					return render(request, 'main_app/index.html')

		return render(request, self.template_name, {'form':form})


class Index(TemplateView):
    template_name = 'main_app/index.html'


class GetCities(APIView):
	# submission throttling
	def get(self, request):
		search = request.GET.get("city", " ")
		print("\n\n\n\n\n", search)

		'''cities = Hotel.objects.city.filter(city__icontains=search)
								print("\n\n\n\n\n", cities)
								return cities'''

		hotels = Hotel.objects.all()
		cities = set()
		for hotel in hotels.iterator():
			if search.lower() in hotel.city.lower():
				cities.add(hotel.city)
		print(cities)
		return JsonResponse(list(cities), safe=False)

class SelectionPage(TemplateView):
	template_name = 'main_app/selection_page.html'

	def post(self, request):
		seat = str(random.randint(1, 40)) + chr(random.randint(65, 77))
		class_ = "Economy"
		flight_name = request.POST.get("flight-name", " ")
		flight = Flight.objects.get(name = flight_name)

		return render(request, self.template_name, {'flight':flight, 'seat':seat, 'class':class_})


class SearchPage(TemplateView):
	template_name = 'main_app/search_page.html'

	def post(self, request):
		departure_city = request.POST.get("departure-city", " ")
		arrival_city = request.POST.get("arrival-city", " ")
		departure_date = request.POST.get("departure-date", " ")

		flights = Flight.objects.all()

		
		flights_dict = []
		for flight in Flight.objects.values():
			flights_dict.append(flight)

		results = []
		for i, flight in enumerate(flights.iterator()): 
			if (departure_city.lower() in flight.departure_city.lower() 
				and arrival_city.lower() in flight.arrival_city.lower()):
				results.append(flights_dict[i])

		

		return render(request, self.template_name, {'results':results})

class LoginPage(TemplateView):
	template_name = 'main_app/login_page.html'

	def post(self, request):
		username = request.POST.get("username", " ")
		password = request.POST.get("password", " ")
		user = authenticate(username=username, password=password)
			
		if user is not None:
			if user.is_active:
				login(request, user)
				request.session['username'] = username
				return render(request, 'main_app/index.html')



		return render(request, self.template_name)
	



