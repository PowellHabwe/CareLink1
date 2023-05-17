
from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    # path('location/', views.location, name='location'),
    # path('hospitals/', views.hospitals_location, name='hospitals_location'),
    path('location/', views.location, name='location'),
    path('nearest/', views.get_nearby_hospitals, name='get_nearby_hospitals'),
    path('nearest2/', views.get_nearby_vacancy_available_hospitals, name='get_nearby_vacancy_available_hospitals'),
    
    path('vehicle/', views.get_nearest_vehicle, name='search_nearby_vehicles'),\
    
    path('fill/', views.fill, name='fill'),

    path('create-appointment/', views.create_appointment_view, name='create_appointment'),

    path('service-payments/', views.service_payments, name='service_payments'),

    path('hired-doctors/', views.hired_doctors, name='hired_doctors'),



    # path('map/', LocationView.as_view(), name='map')

] 