import requests
from django.shortcuts import render, redirect

SEARCH_URL = "https://geocoding-api.open-meteo.com/v1/search"
DETAILS_URL = "https://api.open-meteo.com/v1/forecast"
# Create your views here.


def index(request):
    return render(request, "app/index.html")


def search(request):
    if request.method == "POST":
        location = request.POST.get("location").strip()
        params = {"name": location, "count": 100, "format": "json", "language": "en"}
        result = requests.get(SEARCH_URL, params=params).json()
        res = result.get("results", None)
        return render(
            request,
            "app/result.html",
            {"location": location, "locations": res},
        )
    return redirect("index")


# def details(request, lat, longg):
#     params = {"latitude": lat, "longitude": longg, "hourly": "temperature_2m"}
#     params2 = {"latitude": lat, "longitude": longg, "current": "temperature_2m"}
#     result = request.get(DETAILS_URL, params=params).json()
#     result2 = request.ge(DETAILS_URL, params=params2).json()
#     dates = result.get("hourly", {}).get("time", [])
#     temps = result.get("hourly", {}).get("temperature_2m", [])
#     current_temp = result2["current"]["temperature_2m"]
#     details = {}

#     for i in range(len(dates)):
#         today_date = dates[i].split("T")[0]

#         if today_date not in details:
#             details[today_date] = []

#         details[today_date].append(temps[i])

#     final_data = {}

#     for key, value in details.items():
#         temp = {
#             "min": min(value),
#             "max": max(value),
#             "avg": sum(value) // len(value),
#         }
#         final_data[key] = temp
#     return render(
#         request, "app/details.html", {"details": final_data, "current": current_temp}
#     )


def details(request, name, lat, longg):
    params = {"latitude": lat, "longitude": longg, "hourly": "temperature_2m"}
    params2 = {"latitude": lat, "longitude": longg, "current": "temperature_2m"}

    result = requests.get(DETAILS_URL, params=params).json()
    result2 = requests.get(DETAILS_URL, params=params2).json() 

    dates = result.get("hourly", {}).get("time", [])
    temps = result.get("hourly", {}).get("temperature_2m", [])
    current_temp = result2.get("current", {}).get(
        "temperature_2m", 0
    )  

    details = {}

    for i in range(len(dates)):
        today_date = dates[i].split("T")[0]

        if today_date not in details:
            details[today_date] = []

        details[today_date].append(temps[i])

    final_data = {}

    for key, value in details.items():
        temp = {
            "min": min(value),
            "max": max(value),
            "avg": sum(value) // len(value),
        }
        final_data[key] = temp

    return render(
        request, "app/details.html", {"location": name, "details": final_data, "current": current_temp}
    )
