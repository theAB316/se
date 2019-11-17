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



# Create your views here.
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
	



