from django.shortcuts import render
from storage import load_meters


def meters_list(request):
    meters = load_meters("data/meters.json")
    return render(request, "meters_app/meter_list.html", {"meters": meters})


def meter_detail(request, meter_code):
    meters = load_meters("data/meters.json")
    meter = None
    for m in meters:
        if m.code == meter_code:
            meter = m
            break

    status_code = 404 if meter is None else 200
    return render(request, "meters_app/meter_detail.html",
                  {"meter": meter}, status=status_code)
