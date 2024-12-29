import requests
import geocoder
from datetime import datetime
from flask import Flask, request, render_template, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

llama323Binstructtokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B-Instruct")
llama323Binstructmodel = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B-Instruct")
llama323Binstructtokenizer.pad_token = llama323Binstructtokenizer.eos_token
llama323Binstructmodel = llama323Binstructmodel.to("cuda")


def llama323binstruct_generate_response(prompt):
    print("LLama has been called")
    inputs = llama323Binstructtokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to("cuda")
    print("Generating response")
    with torch.no_grad():
        outputs = llama323Binstructmodel.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=500,
            num_return_sequences=1,
            pad_token_id=llama323Binstructtokenizer.pad_token_id,
        )
    return llama323Binstructtokenizer.decode(outputs[0], skip_special_tokens=True)


def generate_response(prompt):
    return llama323binstruct_generate_response(prompt)


def get_weather_data(lat, lon):
    api_key = "994cf0c0e063cbd38c4d38c27d33b84e"
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"

    try:
        weather_response = requests.get(weather_url)
        aqi_response = requests.get(aqi_url)

        weather_data = weather_response.json()
        aqi_data = aqi_response.json()

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
    except Exception as e:
        return {"error": f"Failed to fetch weather data: {str(e)}"}

app = Flask(__name__)

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
        advice.append("The air quality is poor. If you have allergies, wear a mask and stay indoors.")

    if asthma and aqi != "N/A" and aqi > 100:
        advice.append("The air quality is poor. Limit outdoor activities and carry your inhaler.")

    if sensitive_skin and uv_index != "N/A" and uv_index > 5:
        advice.append("The UV index is high. Apply sunscreen and wear protective clothing.")

    if 6 <= current_hour < 18:
        advice.append("It's daytime. Stay hydrated and use sun protection.")
    else:
        advice.append("It's nighttime. Stay warm and safe.")

    return " ".join(advice)


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

    try:
        weather_description = weather_data['weather']['weather'][0]['description']
        temperature = weather_data['weather']['main']['temp']
    except (KeyError, IndexError, TypeError):
        return "Weather data is not available. Please try again later."

    return render_template(
        'index.html',
        weather_description=weather_description,
        temperature=temperature,
        health_advice=health_advice
    )


@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return {"error": "No message provided"}, 400

    try:
        bot_response = generate_response(user_message)
        return {"response": bot_response}, 200
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == '__main__':
    app.run(debug=True)
