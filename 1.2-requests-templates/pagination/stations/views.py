from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from pagination.settings import BUS_STATION_CSV
import csv

db = []
with open(BUS_STATION_CSV, newline='', encoding='UTF-8') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        db.append({'Name': row['Name'], 'Street': row['Street'], 'District': row['District']})


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    paginator = Paginator(db, 10)
    page_num = int(request.GET.get('page', 1))
    page = paginator.get_page(page_num)

    context = {
        'bus_stations': page.object_list,
        'page': page,
    }

    return render(request, 'stations/index.html', context)
