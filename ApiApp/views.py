from django.http import JsonResponse
import requests

def get_location_and_weather(ip):
    # Use an external API to get the location based on IP address
    location_response = requests.get(f'http://ip-api.com/json/{ip}')
    location_data = location_response.json()

    city = location_data.get('city', 'Unknown location')
    print(f"city: {location_response.text}")
    
    
    weather_api_key = 'b53170003687db34aaab6ec487c93e64'
    weather_response = requests.get(
        f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric'
    )
    weather_data = weather_response.json()
    print(f"Weather: {weather_data}")
    temperature = weather_data['main']['temp']

    return city, temperature

def hello(request):
    visitor_name = request.GET.get('visitor_name', 'Visitor')
    client_ip = request.META.get('REMOTE_ADDR', '127.0.0.1')

    city, temperature = get_location_and_weather(client_ip)

    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"
    response_data = {
        'client_ip': client_ip,
        'location': city,
        'greeting': greeting
    }

    return JsonResponse(response_data)
