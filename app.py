import requests
import geocoder
from datetime import datetime
from textblob import TextBlob
from flask import Flask, request, render_template
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Initialize Llama-3.2-1B-Instruct model and tokenizer
llama323Binstructtokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B-Instruct")
llama323Binstructmodel = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B-Instruct")
llama323Binstructtokenizer.pad_token = llama323Binstructtokenizer.eos_token
llama323Binstructmodel = llama323Binstructmodel.to("cuda")

def get_weather_data(lat, lon):
    api_key = "994cf0c0e063cbd38c4d38c27d33b84e"
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    weather_response = requests.get(weather_url)
    aqi_response = requests.get(aqi_url)

    weather_data = weather_response.json()
    aqi_data = aqi_response.json()

    combined_data = {
        "weather": weather_data,
        "uv_index": weather_data.get("main", {}).get("uvi", "N/A"),
        "aqi": aqi_data["list"][0]["main"]["aqi"] if "list" in aqi_data and len(aqi_data["list"]) > 0 else "N/A",
        "dust_levels": {
            "pm2_5": aqi_data["list"][0]["components"]["pm2_5"] if "list" in aqi_data and len(aqi_data["list"]) > 0 else "N/A",
            "pm10": aqi_data["list"][0]["components"]["pm10"] if "list" in aqi_data and len(aqi_data["list"]) > 0 else "N/A",
        },
    }

    return combined_data


# Function to generate response using the Llama model
def llama323binstruct_generate_response(prompt):
    print("LLama has been called")
    inputs = llama323Binstructtokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to("cuda")
    print("Generating response")
    with torch.no_grad():
        outputs = llama323Binstructmodel.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=700,
            num_return_sequences=1,
            pad_token_id=llama323Binstructtokenizer.pad_token_id,
        )

    return llama323Binstructtokenizer.decode(outputs[0], skip_special_tokens=True)


def generate_response(prompt):
    prompt = prompt
    return llama323binstruct_generate_response(prompt)


# Function to provide health advice based on weather data
def get_health_advice(weather_data, allergies=None, asthma=None, sensitive_skin=False):
    try:
        main = weather_data['weather']['weather'][0]['main']
        temp = weather_data['weather']['main']['temp']
        uv_index = weather_data.get("uv_index", "N/A")
        aqi = weather_data.get("aqi", "N/A")
    except (KeyError, IndexError, TypeError):
        return "Weather data is not available. Please try again later."

    advice = ["Stay hydrated and take care of your health!"]
    current_hour = datetime.now().hour

    if allergies and aqi != "N/A" and aqi > 100:
        advice.append(
            "The air quality is poor. If you have allergies, wear a mask to filter out pollutants and stay indoors when possible.")

    if asthma:
        if aqi != "N/A" and aqi > 100:
            advice.append(
                "The air quality is poor. People with asthma should limit outdoor activities and wear a mask to prevent inhaling pollutants.")
        if temp < 0 or temp > 35:
            advice.append(
                "Extreme temperatures can trigger asthma symptoms. Carry your inhaler and avoid sudden temperature changes.")

    if sensitive_skin:
        if uv_index != "N/A" and uv_index > 5:
            advice.append(
                "The UV index is high. Apply sunscreen every 2 hours, wear tinted glasses, and use a wide-brimmed hat for sun protection.")

    if 6 <= current_hour < 18:
        advice.append("It's daytime. Drink plenty of water, wear sunglasses, and apply sunscreen if you're going outside.")
    else:
        advice.append("It's nighttime. Ensure you stay warm and safe if you're going out.")

    if main == 'Clear':
        if temp > 30:
            advice.append(
                "It's sunny and hot. Wear a hat, sunglasses, and apply sunscreen. Stay hydrated and avoid being outside during peak sun hours (10 AM - 4 PM).")
        else:
            advice.append("It's a clear day. Enjoy outdoor activities, but take necessary precautions like sunscreen.")
    elif main == 'Rain':
        advice.append("It's raining. Carry an umbrella and wear waterproof shoes.")
    elif main == 'Snow':
        advice.append("It's snowing. Dress warmly, and wear insulated gloves and a hat.")
    elif main == 'Clouds':
        advice.append(
            "It's cloudy. A comfortable day for outdoor activities, but keep an umbrella handy in case of unexpected rain.")
    else:
        advice.append("Stay safe and follow general weather precautions.")

    if temp < 5:
        advice.append("It's very cold. Wear layers, gloves, and a scarf to stay warm.")
    if temp > 35:
        advice.append("It's very hot. Avoid overexertion, stay in shaded areas, and drink plenty of fluids.")
    if aqi != "N/A" and aqi > 200:
        advice.append("The air quality is very poor. Avoid outdoor activities, close windows, and consider using an air purifier indoors.")

    return " ".join(advice)


# Flask app setup
app = Flask(__name__)

@app.route('/')
def home():
    g = geocoder.ip('me')
    if g.latlng is None:
        return "Could not get your location. Please try again later."

    lat, lon = g.latlng
    weather_data = get_weather_data(lat, lon)
    allergies = request.args.get('allergies', False)
    asthma = request.args.get('asthma', False)
    sensitive_skin = request.args.get('sensitive_skin', False)

    health_advice = get_health_advice(weather_data, allergies=allergies, asthma=asthma, sensitive_skin=sensitive_skin)
    health_advice = TextBlob(health_advice)

    try:
        weather_description = weather_data['weather']['weather'][0]['description']
        temperature = weather_data['weather']['main']['temp']
    except (KeyError, IndexError, TypeError):
        return "Weather data is not available. Please try again later."

    uv_index = weather_data.get("uv_index", "N/A")
    aqi = weather_data.get("aqi", "N/A")
    pm2_5 = weather_data["dust_levels"].get("pm2_5", "N/A")
    pm10 = weather_data["dust_levels"].get("pm10", "N/A")

    return render_template(
        'index.html',
        weather_description=weather_description,
        temperature=temperature,
        uv_index=uv_index,
        aqi=aqi,
        pm2_5=pm2_5,
        pm10=pm10,
        health_advice=health_advice
    )

@app.route('/chatbot', methods=['POST'])
def chatbot():
    g = geocoder.ip('me')
    if g.latlng is None:
        return "Could not get your location. Please try again later."

    lat, lon = g.latlng
    weather_data = get_weather_data(lat, lon)
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return {"error": "No message provided"}, 400

    try:
        def get_weather_context_string():
            try:
                weather = weather_data['weather']['weather'][0]['description']
                temperature = weather_data['weather']['main']['temp']
                uv_index = weather_data.get("uv_index", "N/A")
                aqi = weather_data.get("aqi", "N/A")
                pm2_5 = weather_data["dust_levels"].get("pm2_5", "N/A")
                pm10 = weather_data["dust_levels"].get("pm10", "N/A")

                context = (
                    f"Current weather is {weather} with a temperature of {temperature}°C. "
                    f"The UV index is {uv_index}. "
                    f"The air quality index (AQI) is {aqi}. "
                    f"PM2.5 levels are {pm2_5}, and PM10 levels are {pm10}."
                )
                return context
            except (KeyError, IndexError, TypeError):
                return "Weather context data is unavailable. Please try again later."
        bot_response = generate_response(user_message+get_weather_context_string())
        return {"response": bot_response}, 200
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
