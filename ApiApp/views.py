from django.http import JsonResponse
import requests

def get_ip():
    try:
        response = requests.get('https://api64.ipify.org?format=json', timeout=5)
        response.raise_for_status()
        return response.json()["ip"]
    except requests.RequestException:
        return '127.0.0.1'

def get_location(ip):
    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/', timeout=5)
        response.raise_for_status()
        location_data = response.json()
        city = location_data.get("city", "Unknown city")
        
        weather_api_key = 'b53170003687db34aaab6ec487c93e64'
        weather_response = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric', timeout=5
        )
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        temperature = weather_data['main']['temp']
        
        return {
            "ip": ip,
            "city": city,
            "region": location_data.get("region"),
            "country": location_data.get("country_name")
        }, temperature
    except requests.RequestException:
        return {
            "ip": ip,
            "city": "Unknown city",
            "region": "Unknown region",
            "country": "Unknown country"
        }, "N/A"

def hello(request):
    visitor_name = request.GET.get('visitor_name', 'Visitor')
    client_ip = get_ip()

    location_data, temperature = get_location(client_ip)

    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location_data['city']}"
    response_data = {
        'client_ip': client_ip,
        'location': location_data,
        'greeting': greeting
    }

    return JsonResponse(response_data)
