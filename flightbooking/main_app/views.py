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
from .forms import UserForm, UserDetailsForm

from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags



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
		res_id = request.GET.get("id", " ")
		print("\n\n\n\n\n", search)

		'''cities = Hotel.objects.city.filter(city__icontains=search)
								print("\n\n\n\n\n", cities)
								return cities'''

		flights = Flight.objects.all()
		cities = set()
		for flight in flights.iterator():
			if res_id == "city1" and search.lower() in flight.departure_city.lower():
				cities.add(flight.departure_city)
			elif res_id == "city2" and search.lower() in flight.arrival_city.lower():
				cities.add(flight.arrival_city)
		print(cities)
		return JsonResponse(list(cities), safe=False)

class TicketPage(TemplateView):
	template_name = 'main_app/ticket_page2.html'

	def post(self, request):
		first_name = request.POST.get("first_name", " ")
		last_name = request.POST.get("last_name", " ")
		age = request.POST.get("age", " ")
		receiver_email = request.POST.get("email", " ")
		request.session['receiver_email'] = receiver_email
		gender = request.POST.get("gender", " ")


		seat = str(random.randint(1, 40)) + chr(random.randint(65, 77))
		class_ = "Economy"
		flight_name = request.POST.get("flight_name", " ")
		flight = Flight.objects.get(name = flight_name)

		print("\n\n\n", flight)

		results = {'flight':flight, 'seat':seat, 'class':class_, 
				   'first_name':first_name, 'last_name':last_name, 'age':age, 'gender':gender}

		'''email = EmailMessage('Here is your ticket from Make My Flight!','balu', 'balubadmash123@gmail.com', to=[receiver_email])
								email.send()'''

		return render(request, self.template_name, {'results':results})


class SearchPage(TemplateView):
	template_name = 'main_app/search_page.html'

	def post(self, request):
		departure_city = request.POST.get("departure-city", " ")
		arrival_city = request.POST.get("arrival-city", " ")
		departure_date = request.POST.get("departure-date", " ")

		request.session["passengers"] = request.POST.get("passengers", " ")

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

class SelectionPage(TemplateView):
	template_name = 'main_app/selection_page2.html'

	def post(self, request):
		flight_name = request.POST.get("flight-name", " ")
		flight = Flight.objects.get(name = flight_name)

		request.session["flight_name"] = flight_name

		request.session["departure_time"] = str(flight.departure_time)
		request.session["arrival_time"] = str(flight.arrival_time)

		request.session["departure_city"] = str(flight.departure_city)
		request.session["arrival_city"] = str(flight.arrival_city)



		return render(request, self.template_name, {'flight':flight})
	

class UserDetailsView(TemplateView):
	form_class = UserDetailsForm
	template_name = 'main_app/userdetails_page.html'

	#after submit
	def post(self, request):
		flight_name = request.session.get("flight_name", " ")
		flight = Flight.objects.get(name=flight_name)

		departure_city = flight.departure_city
		arrival_city = flight.arrival_city

		departure_time = flight.departure_time
		arrival_time = flight.arrival_time
		
		#might need session

		data_dict = {'flight_name': flight_name,
		 'departure_city': departure_city,'arrival_city': arrival_city,
		 'departure_time': departure_time,'arrival_time': arrival_time,
		 }
		form = self.form_class(data_dict)
		form.fields['flight_name'].widget.attrs['readonly'] = True
		form.fields['departure_city'].widget.attrs['readonly'] = True
		form.fields['arrival_city'].widget.attrs['readonly'] = True
		form.fields['departure_time'].widget.attrs['readonly'] = True
		form.fields['arrival_time'].widget.attrs['readonly'] = True

		return render(request, self.template_name, {'form':form})

class SendMailPage(APIView):
	template_name = 'main_app/ticket_page2.html'
	def get(self, request):
		'''subject = "Here is your ticket from Make My Flight"
						
								dictionary = {"results.flight.name" : request.session['flight_name']}
						
								html_content = render_to_string(self.template_name, dictionary) # render with dynamic value
								text_content = strip_tags(html_content) # Strip the html tag. So people can see the pure text at least.
								
								from_email = "balubadmash123@gmail.com"
								to = request.session['receiver_email']
								
								msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
								msg.attach_alternative(html_content, "text/html")
								msg.send()'''
		
		from_email = "balubadmash123@gmail.com"
		title = "Here is your ticket from Make My Flight"
		body = "Flight: " + str(request.session["flight_name"]) \
			+ "\n"+ "Departure time:" \
			+ str(request.session["departure_time"]) \
			+ "\n"+ "Arrival time:" + str(request.session["arrival_time"]) \
			+ "\n"
		
		to = request.session['receiver_email']
		email = EmailMessage(title, body, from_email, to=[to])
		email.send()
		return HttpResponse()


