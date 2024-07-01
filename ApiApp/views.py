from django.http import JsonResponse
import requests

def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_location(request):
    try:
        ip_address = get_ip(request) # getting ip address
        location_data = requests.get(f'https://ipapi.co/{ip_address}/json/').json() # uses the ip address to  get information 
        
        city = location_data.get("city")
        
        weather_api_key = 'b53170003687db34aaab6ec487c93e64'
        weather_response = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric', timeout=20
        )
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        temperature = weather_data['main']['temp']
        
        return {
            "ip": ip_address,
            "city": city,
            "region": location_data.get("region"),
            "country": location_data.get("country_name")
        }, temperature
    except requests.RequestException:
        return {
            "ip": ip_address,
            "city": "Unknown city",
            "region": "Unknown region",
            "country": "Unknown country"
        }, "N/A"

def hello(request):
    visitor_name = request.GET.get('visitor_name', 'Visitor')
    client_ip = get_ip(request)

    location_data, temperature = get_location(request)

    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location_data['city']}"
    response_data = {
        'client_ip': client_ip,
        'location': location_data,
        'greeting': greeting
    }

    return JsonResponse(response_data)
