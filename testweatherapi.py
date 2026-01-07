import requests

API_KEY = "80ad0124410dd85906904a668d52b0b8"
ville = "Seattle"

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=fr"
    response = requests.get(url).json()
    return response

weather = get_weather(ville)

# Vérifier la réponse complète
print(weather) 

