from django.urls import path

from . import views
app_name = 'main_app'

urlpatterns = [
    path('', views.Index.as_view(), name = 'Index'),
    path('search_page', views.SearchPage.as_view(), name='SearchPage'),
    path('login_page', views.LoginPage.as_view(), name='LoginPage'),
    path('get_cities', views.GetCities.as_view(), name = 'GetCities'),
    path('selection_page', views.SelectionPage.as_view(), name = 'SelectionPage'),

]