from django.shortcuts import render
from .forms import AddressForm
from .models import GeocodedAddress
import requests
import json


def geocoder_view(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            response = requests.get(f'https://nominatim.openstreetmap.org/search?format=json&q={address}')
            data = response.json()
            print (data)
            if data:
                lat = data[0]['lat']
                lon = data[0]['lon']
                GeocodedAddress.objects.create(address=address, latitude=lat, longitude=lon)
    else:
        form = AddressForm()
    addresses = GeocodedAddress.objects.all()
    return render(request, 'index.html', {'form': form, 'addresses': addresses})

