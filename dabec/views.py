from django.shortcuts import render
from store.models import Hospital
def home(request):
    home_general = Hospital.objects.all().filter(home_general = True)
    home_specialty = Hospital.objects.all().filter(home_specialty = True)
    home_psychiatric = Hospital.objects.all().filter(home_psychiatric = True)
    home_clinic = Hospital.objects.all().filter(home_clinic = True)

    top_rated = Hospital.objects.all().filter(top_rated = True)
    new = Hospital.objects.all().filter(new = True)
    context = {
        'home_general': home_general,
        'home_specialty':home_specialty,
        'top_rated':top_rated,
        'new':new,
        'home_psychiatric': home_psychiatric,
        'home_clinic':home_clinic,
    }
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'includes/aboutus.html')