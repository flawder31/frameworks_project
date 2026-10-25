from django.shortcuts import render
from storage import load_meters, load_readings


def readings_list(request):
    meters = load_meters("data/meters.json")
    readings = load_readings("data/readings.json", meters)
    return render(request, "readings_app/reading_list.html", {"readings": readings})
