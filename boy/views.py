import requests
from django.http import JsonResponse
from django.views import View
from django.conf import settings


class GreetView(View):
    def get(self, request):
        clients_name = request.GET.get("clients_name", "Client")
        client_ip = request.META.get('REMOTE_ADDR')

        # Using a mock IP for location data
        mock_ip = client_ip if client_ip != '127.0.0.1' else '8.8.8.8'

        try:
            location_response = requests.get(f'http://ip-api.com/json/{mock_ip}')
            location_response.raise_for_status()
            location_data = location_response.json()
        except (requests.RequestException, ValueError):
            location_data = {}

        location = location_data.get('city', 'Unknown')
        lat = location_data.get('lat', 0)
        lon = location_data.get('lon', 0)

        # Real-time weather report using Weather.com API
        weather_api_key = settings.WEATHER_API_KEY
        weather_url = f"https://api.weather.com/v3/wx/conditions/current?geocode={lat},{lon}&format=json&apiKey={weather_api_key}&language=en-US"

        try:
            weather_response = requests.get(weather_url)
            weather_response.raise_for_status()
            weather_data = weather_response.json()
        except (requests.RequestException, ValueError):
            weather_data = {}

        temperature = weather_data.get('temperature', 'N/A')

        greeting = f"Welcome Senior Man, {clients_name}!"
        weather = f"The temperature is {temperature} degrees Celsius"
        response = {
            "ip": client_ip,
            "location": location,
            "greeting": greeting,
            "weather report": weather
        }

        return JsonResponse(response)
