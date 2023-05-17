from django.shortcuts import render, redirect
import requests
from geocoder import ip
from store.models import Hospital
from math import radians, cos, sin, asin, sqrt
from geocoder import geocode

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def get_nearest_hospitals(request):
    if request.method == 'POST':
        # Get user's location using geocoder
        user_location = geocode(request.META['REMOTE_ADDR'])

        user_lat = user_location.latitude
        user_lon = user_location.longitude

        # Get all hospitals
        hospitals = Hospital.objects.all()

        # Calculate the distance from user's location to each hospital
        for hospital in hospitals:
            hospital_lat = hospital.latitude
            hospital_lon = hospital.longitude
            distance = haversine(user_lat, user_lon, hospital_lat, hospital_lon)
            hospital.distance = distance

        # Sort hospitals by distance
        sorted_hospitals = sorted(hospitals, key=lambda x: x.distance)

        return render(request, '/directions/nearest_hospitals.html', {'hospitals': sorted_hospitals})
    else:
        return render(request, '/directions/get_location.html')
