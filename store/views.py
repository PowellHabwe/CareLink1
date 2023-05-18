from django.shortcuts import render, get_object_or_404, redirect
from store.models import Hospital,Vehicle,Doctor,Service,ServiceProvided, PaymentService, Appointment, HospitalService
from accounts.models import Account
from category.models import Category
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from googlemaps import Client
import googlemaps
import math
import requests
import json


# Create your views here.

def store(request, category_slug=None):
    categories = None
    hospitals = None

    if category_slug !=None:
        categories = get_object_or_404(Category, slug=category_slug)
        hospitals = Hospital.objects.all().filter(category = categories, is_available=True)
    else:
        hospitals = Hospital.objects.all().filter(is_available=True)
    context = {
        'hospitals': hospitals,
    }
    
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Hospital.objects.get(category__slug=category_slug,slug=product_slug)
        
    except Exception as e:
        raise e
        
    context = {
        'single_product':single_product,
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            hospitals = Hospital.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = hospitals.count()

    context = {
        'hospitals':hospitals,
        'product_count':product_count
    }
    return render(request, 'store/store.html', context)



# LOCATION BASED SERVICES

def location(request):
    ip = requests.get('https://api.ipify.org?format=json')
    ip_data = json.loads(ip.text)
    res = requests.get('http://ip-api.com/json/' + ip_data["ip"])
    location_data_one = res.text
    location_data = json.loads(location_data_one)

    response_data = {
        'latitude': location_data['lat'],
        'longitude': location_data['lon']
    }

    hospitals = get_nearby_hospitals(latitude=location_data['lat'], longitude=location_data['lon'])

    return JsonResponse(hospitals, safe=False)

    
def get_nearby_hospitals(request):
    ip = requests.get('https://api.ipify.org?format=json')
    ip_data = json.loads(ip.text)
    res = requests.get('http://ip-api.com/json/' + ip_data["ip"])
    location_data_one = res.text
    location_data = json.loads(location_data_one)


    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

    # Perform a nearby search for hospitals
    result = gmaps.places_nearby(
        location=(location_data['lat'], location_data['lon']),
        radius=2000,
        keyword='hospital',
        type='hospital'
    )

    # Extract the necessary information from the results
    hospitals = []
    for place in result.get('results', []):
        name = place.get('name')
        address = place.get('vicinity')


        hospitals.append({'name': name, 'address': address})
        print('hospitals', hospitals)

    return JsonResponse(hospitals, safe=False)



def get_vacancy_available_hospitals(request):
    database_hospitals = Hospital.objects.filter(vacancies_available=True)
    vacancy_available_hospitals = []
    
    for hospital in database_hospitals:
        vacancy_available_hospitals.append({
            'name': hospital.hospital_name,
            'address': hospital.location,
            'ambulance_contacts': hospital.ambulance_contacts
        })

    return vacancy_available_hospitals


# GET NEAREST HOSPITAL DATA

@csrf_exempt
def get_nearby_vacancy_available_hospitals(request):
    ip = requests.get('https://api.ipify.org?format=json')
    ip_data = json.loads(ip.text)
    res = requests.get('http://ip-api.com/json/' + ip_data["ip"])
    location_data_one = res.text
    location_data = json.loads(location_data_one)
    gmaps = Client(key=settings.GOOGLE_MAPS_API_KEY)
    available = Hospital.objects.all().filter(home_available = True)

    # Get the user's location
    user_location = location_data

    # Get the list of all hospitals within a certain radius of the user's location
    result = gmaps.places_nearby(
        location=(user_location['lat'], user_location['lon']),
        radius=2000,
        keyword='hospital',
        type='hospital'
    )

    # Filter the list of hospitals based on the vacancyavailable boolean
    vacancy_available_hospitals = []
    for place in result.get('results', []):
        name = place.get('name').lower()  # Convert the name to lowercase
        address = place.get('vicinity')
        try:
            hospital = Hospital.objects.get(hospital_name__iexact=name)
            if hospital.vacancies_available:
                hospital_data = {'name': name, 'address': address, 'phone_number': hospital.phone_number, 'ambulance_available': hospital.ambulance_available}
                if hospital.ambulance_available:
                    # Check if the hospital already exists in the list
                    existing_hospital = next(
                        (
                            h
                            for h in vacancy_available_hospitals
                            if h['name'].lower() == name and h['address'] == address  # Compare lowercase names
                        ),
                        None
                    )
                    if existing_hospital:
                        # Update the ambulance_contacts field if the hospital already exists
                        existing_hospital['ambulance_contacts'] = hospital.ambulance_contacts
                    else:
                        # Append a new hospital to the list if it doesn't exist
                        hospital_data['ambulance_contacts'] = hospital.ambulance_contacts
                        vacancy_available_hospitals.append(hospital_data)
        except Hospital.DoesNotExist:
            # Handle the case when the hospital is not found in the database
            pass

    # Return the list of nearby vacancy available hospitals
    return render(request, 'store/hospital_location.html', {'hospitals': vacancy_available_hospitals, 'available':available})

# NEAREST VEHICLE AVAILABLE

# def get_nearest_vehicle(request):
#     user_location = get_user_location(request)
#     user_latitude = user_location['latitude']
#     user_longitude = user_location['longitude']

#     # Get the nearest available vehicle
#     nearest_vehicle = None
#     nearest_distance = math.inf

#     available_vehicles = Vehicle.objects.filter(availability=True)
#     for vehicle in available_vehicles:
#         distance = calculate_distance(user_latitude, user_longitude, vehicle.latitude, vehicle.longitude)
#         if distance < nearest_distance:
#             nearest_distance = distance
#             nearest_vehicle = vehicle

#     if nearest_vehicle:
#         vehicle_info = {
#             'vehicle_type': nearest_vehicle.vehicle_type,
#             'vehicle_name': nearest_vehicle.vehicle_name,
#             'latitude': nearest_vehicle.latitude,
#             'longitude': nearest_vehicle.longitude,
#             'contact': nearest_vehicle.contact,
#             'distance': nearest_distance
#         }
#         return JsonResponse(vehicle_info)

#     return JsonResponse({'message': 'No available vehicles nearby.'})

def get_nearest_vehicle(request, limit=5):
    user_location = get_user_location(request)
    user_latitude = user_location['latitude']
    user_longitude = user_location['longitude']

    # Get the available vehicles
    available_vehicles = Vehicle.objects.filter(availability=True)

    # Calculate distances for all vehicles
    vehicle_distances = []
    for vehicle in available_vehicles:
        distance = calculate_distance(user_latitude, user_longitude, vehicle.latitude, vehicle.longitude)
        distance = distance / 1000
        distance = round(distance, 2)
        vehicle_distances.append((vehicle, distance))

    # Sort vehicles by distance (from nearest to farthest)
    vehicle_distances.sort(key=lambda x: x[1])

    # Prepare response data for the nearest vehicles
    nearest_vehicles = []
    for vehicle, distance in vehicle_distances[:limit]:
        vehicle_info = {
            'vehicle_type': vehicle.vehicle_type,
            'vehicle_name': vehicle.vehicle_name,
            'latitude': vehicle.latitude,
            'longitude': vehicle.longitude,
            'contact': vehicle.contact,
            'price': vehicle.price_per_km,
            'distance': distance
        }
        nearest_vehicles.append(vehicle_info)

    if nearest_vehicles:
        return render(request, 'directions/nearest_vehicle.html', {'nearest_vehicles': nearest_vehicles})

    return render(request, 'directions/nearest_vehicle.html', {'message': 'No available vehicles nearby.'})

def get_user_location(request):
    ip = requests.get('https://api.ipify.org?format=json')
    ip_data = json.loads(ip.text)
    res = requests.get('http://ip-api.com/json/' + ip_data["ip"])
    location_data_one = res.text
    location_data = json.loads(location_data_one)

    user_location = {
        'latitude': location_data['lat'],
        'longitude': location_data['lon']
    }

    return user_location


def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert coordinates to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    earth_radius = 6371  # Radius of the Earth in kilometers
    distance_km = earth_radius * c
    distance_m = distance_km * 1000  # Convert distance to meters

    return distance_m


# online booking
def fill(request):
    return render(request, 'appointments/appointment_form.html')


def create_appointment_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        service_name = request.POST.get('service')
        hospital_name = request.POST.get('hospital')

        # Query the HospitalService model to find a matching service and hospital
        try:
            hospital_service = HospitalService.objects.get(service__name__iexact=service_name, hospital__hospital_name__iexact=hospital_name)
        except HospitalService.DoesNotExist:
            # Handle the case when the service or hospital is not found
            return render(request, 'appointments/appointment_form.html')

        # Decrement the slots field of the matched HospitalService record
        hospital_service.slots -= 1
        hospital_service.save()

        # Create and save the appointment
        appointment = Appointment.objects.create(name=name, service=hospital_service.service, hospital=hospital_service.hospital)

        # Redirect to a success page or display a success message
        return redirect('appointment_success.html')

    return render(request, 'appointments/appointment_form.html')

# service servie agreement
def service_page(request):
    return render(request, 'payment/service_payments.html')



def service_payments(request):
    if request.method == 'POST':
        hospital_id = request.POST.get('hospital')
        service = request.POST.get('service')
        payment_method = request.POST.get('payment_method')
        name = request.POST.get('name')
        email = request.POST.get('email')

        # Save the provided service data to the ServiceProvided model
        service_provided = ServiceProvided.objects.create(hospital_id=hospital_id, service=service, payment_method=payment_method, name=name, email=email)

        # Redirect to a success page or render a confirmation message
        return render(request, 'payment/service_provided.html', {'name': name})
    else:
        # Handle GET request
        payment_services = PaymentService.objects.all()
        return render(request, 'payment/service_payments.html', {'payment_services': payment_services})
    


def hired_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'temp_hirings/hired_doctors.html', {'doctors': doctors})








