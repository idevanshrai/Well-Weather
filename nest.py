import requests
import geocoder


def get_weather_data(lat, lon):
    api_key = "994cf0c0e063cbd38c4d38c27d33b84e"  # Replace with your OpenWeatherMap API key
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"

    try:
        # Request weather data
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()  # Raise HTTPError if the request failed

        # Request air quality data
        aqi_response = requests.get(aqi_url)
        aqi_response.raise_for_status()  # Raise HTTPError if the request failed

        weather_data = weather_response.json()
        aqi_data = aqi_response.json()

        # Combine relevant weather and AQI data
        combined_data = {
            "weather": weather_data,
            "uv_index": weather_data.get("main", {}).get("uvi", "N/A"),
            "aqi": aqi_data["list"][0]["main"]["aqi"] if "list" in aqi_data and len(aqi_data["list"]) > 0 else "N/A",
            "dust_levels": {
                "pm2_5": aqi_data["list"][0]["components"]["pm2_5"] if "list" in aqi_data and len(
                    aqi_data["list"]) > 0 else "N/A",
                "pm10": aqi_data["list"][0]["components"]["pm10"] if "list" in aqi_data and len(
                    aqi_data["list"]) > 0 else "N/A"
            }
        }

        return combined_data

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


# Get user's location
g = geocoder.ip('me')
if g.latlng:
    lat, lon = g.latlng
    weather_info = get_weather_data(lat, lon)
    print(weather_info)
else:
    print("Could not determine your location. Please try again.")
