import requests
# OpenWeatherMap API configuration
api_key = "b963de19cb57f49a5a04788439d47db3"
base_url = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(location):
	# Construct the API request URL
	params = {
		"q": location,
		"appid": api_key,
		"units": "metric"  # Request temperature in Celsius
	}
	response = requests.get(base_url, params=params)
	data = response.json()

	# Extract relevant weather information
	temperature = data['main']['temp']
	humidity = data['main']['humidity']
	weather_description = data['weather'][0]['description']

	# Format the weather information into a response
	weather_info = f"The current weather in {location} is {weather_description}. " \
	               f"The temperature is {temperature}°C with a humidity of {humidity}%."
	return weather_info
