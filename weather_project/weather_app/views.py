from django.shortcuts import render
import requests
import datetime

def index(request):

    current_weather_url = "https://geocoding-api.open-meteo.com/v1/search?name={}&count=1&language=en&format=json"
    forecast_url = "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&current=temperature_2m&daily=temperature_2m_max,temperature_2m_min&timezone=auto&forecast_days=7"

    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, current_weather_url, forecast_url)

        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, current_weather_url,
                                                                         forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        context = {
            'weather_data1': weather_data1,
            'daily_forecasts1': daily_forecasts1,
            'weather_data2': weather_data2,
            'daily_forecasts2': daily_forecasts2,
        }

        return render(request, 'weather_app/index.html', context)
    else:
        return render(request, 'weather_app/index.html')


def fetch_weather_and_forecast(city, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city)).json()
    lat, lon = response['results'][0]['latitude'], response['results'][0]['longitude']
    forecast_response = requests.get(forecast_url.format(lat, lon)).json()


    weather_data = {
        'city': city,
        'time':forecast_response['current']['time'],
        'temperature': forecast_response['current']['temperature_2m']
    }

    daily_forecasts = []
    for i in range(7):
        daily_forecasts.append({
            'day': forecast_response['daily']['time'][i],
            'min_temp': forecast_response['daily']['temperature_2m_min'][i],
            'max_temp': forecast_response['daily']['temperature_2m_max'][i]
        })


    return weather_data, daily_forecasts