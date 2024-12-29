# WellWeather - A Weather-Related Health Advisor

## Overview
**WellWeather** is a web application designed to provide comprehensive health advice based on current weather conditions and a user's health profile. Combining real-time weather data, air quality indexes (AQI), and user-specific health concerns (e.g., asthma, sensitive skin, allergies), **WellWeather** acts as a weather-related health advisor to help users make informed decisions about their day-to-day activities.

The application also includes a natural language chatbot that enables users to engage in conversational interactions for weather or health-related queries. This platform is ideal for individuals interested in proactively managing their health based on environmental conditions.

---

## Features
### 1. **Real-Time Weather Insights**
- Fetches current weather data alongside UV index, temperature, and forecasts using the OpenWeatherMap API.
- Retrieves air quality information (AQI) and detailed dust pollution data (PM2.5, PM10).

### 2. **Health Advice Based on Weather**
- Offers health recommendations for users based on weather data as well as their personal health considerations:
  - **Allergies:** Provides advice to reduce exposure during poor air quality.
  - **Asthma:** Suggestions to avoid outdoor activities during adverse air conditions or extreme temperatures.
  - **Sensitive Skin:** Special care tips for UV protection and skin safety.
- Responds dynamically to weather changes such as rain, snow, or high temperatures with tailored advice.

### 3. **Chatbot Integration**
- A natural language chatbot powered by a fine-tuned LLaMA-3.2 model.
- Allows users to interact conversationally to ask questions about weather or health tips.
- User-friendly, AI-based responses for complex queries.

### 4. **Location-Based Automation**
- Automatically fetches the user's geographic location using IP-based geocoding to provide localized weather insights and advice.

### 5. **User-Friendly Interface**
- A web-based interface allowing easy interaction with weather data, health advice, and chatbot dialogue in a simple and visually appealing format.

---

## Technical Details
### Tech Stack
- **Backend Framework:** Flask (for server-side handling and API routing)
- **Frontend:** HTML templates with Jinja2 for dynamic rendering
- **APIs:**
  - [OpenWeatherMap API](https://openweathermap.org/) for weather and air quality data
  - [Geocoder](https://geocoder.readthedocs.io/) for location-based queries
- **Model Integration:** Transformer models like GPT-2 and LLaMA-3.2 for natural language understanding (NLU)
- **Libraries:**
  - `requests` for API integration
  - `spacy` and `TextBlob` for text processing and advice generation
  - `pytorch` for inference on the LLaMA model

### Key Functionalities
1. **Weather Data Retrieval (`get_weather_data`)**
   - Combines data from multiple OpenWeatherMap API endpoints to provide a holistic view of weather and pollution conditions.
   - Returns a unified JSON structure with weather stats, AQI, UV index, and dust levels.

2. **Health Advice Generator (`get_health_advice`)**
   - Evaluates weather conditions and user-specific health parameters (like allergies or sensitive skin) to provide actionable health advice.
   - Categorizes advice based on scenarios such as extreme temperatures, poor air quality, or high UV levels.

3. **Chatbot (`chatbot`)**
   - Employs a tailored language model for generating context-aware replies to user queries.
   - Acts as a conversational interface for health and weather-related interactions.

4. **Flask Routes**
   - `/`: Primary landing page that fetches user location and displays weather updates along with health advice.
   - `/chatbot`: Endpoint for receiving chatbot-related queries (POST).

---

## How to Run Locally
1. **Prerequisites:**
   - Python 3.10 or higher installed.
   - Install the required dependencies using the following command:
     ```bash
     pip install -r requirements.txt
     ```
   - Replace the placeholder `API_KEY` attributes in the code with your OpenWeatherMap API key.

2. **Running the Application:**
   - Start the Flask application:
     ```bash
     python app.py
     ```
   - Accessible on `http://localhost:5000` in your browser.

3. **API Testing:**
   - Use a tool such as `Postman` or `cURL` to send a POST request to `/chatbot`:
     ```json
     {
       "message": "What precautions should I take in hot weather?"
     }
     ```

---

## Possible Use Cases
- **Personal Health and Safety:** Equip users with real-time health advice for varying environmental scenarios (e.g., sunburn risk on sunny days, pollutant awareness, etc.).
- **Elderly and At-Risk Individuals:** Help vulnerable populations manage ailments exacerbated by poor weather conditions.
- **Outdoor Enthusiasts:** Offer advice to those planning their day based on weather and air quality.

---

## Future Enhancements
- **Authentication:** Allow users to save preferences (e.g., allergy profiles) for a personalized experience.
- **Calendar Integration:** Provide weather-based scheduling advice for events.
- **Broader Model Enhancements:** Extend natural language processing (NLP) capabilities for deep weather-health conversations.
- **Localization:** Multi-language support for non-English-speaking users.

---

## Getting Help
For issues, bugs, or feature requests, please create an issue in the project's repository, or contact the maintainers.

---
