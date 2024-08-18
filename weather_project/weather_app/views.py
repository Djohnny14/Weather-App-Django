from django.shortcuts import render
import requests

def index(request):

    coordinate_url = "https://geocoding-api.open-meteo.com/v1/search?name={}&count=1&language={}&format=json"
    forecast_url = "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&current=temperature_2m&daily=temperature_2m_max,temperature_2m_min&timezone=auto&forecast_days=7"

    if request.method == 'POST':
        city = request.POST['city']
        lang=request.POST.get('lang')
        weather_data, daily_forecasts = fetch_weather_and_forecast(city, lang, coordinate_url, forecast_url)
        context = {
            'weather_data': weather_data,
            'daily_forecasts': daily_forecasts,
        }
        return render(request, 'weather_app/index.html', context)
    else:
        return render(request, 'weather_app/index.html')


def fetch_weather_and_forecast(city, lang, coordinate_url, forecast_url):
    response = requests.get(coordinate_url.format(city,lang)).json()
    lat, lon = response['results'][0]['latitude'], response['results'][0]['longitude']
    # print(f'Latitude:{lat}; Longitude:{lon}')
    forecast_response = requests.get(forecast_url.format(lat, lon)).json()

    weather_data = {
        'city': city,
        'time':forecast_response['current']['time'][-5::],
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