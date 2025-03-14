import streamlit as st
import requests
import os
from langchain_community.llms import HuggingFaceEndpoint

# Set your API keys (Replace with your actual OpenWeather API key)
OPENWEATHER_API_KEY = "e370bc4c82f808e76c575b8899e3540f"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

# Initialize Hugging Face LLM
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct",
    task="text-generation",
    temperature=0.6
)

# Weather condition-based backgrounds
WEATHER_BACKGROUNDS = {
    "clear": "#FFD700",  # Sunny - Gold
    "clouds": "#A9A9A9",  # Cloudy - Dark Gray
    "rain": "#4682B4",  # Rainy - Steel Blue
    "thunderstorm": "#4B0082",  # Thunderstorm - Indigo
    "snow": "#ADD8E6",  # Snow - Light Blue
    "mist": "#D3D3D3",  # Mist - Light Gray
    "default": "#FFFFFF"  # Default - White
}

# Weather condition-based emojis/icons
WEATHER_ICONS = {
    "clear": "☀️",
    "clouds": "☁️",
    "rain": "🌧️",
    "thunderstorm": "⛈️",
    "snow": "❄️",
    "mist": "🌫️",
    "default": "❓"
}

# Function to get weather data
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?appid={OPENWEATHER_API_KEY}&q={city}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        weather_condition = data['weather'][0]['main'].lower()  # Get main condition in lowercase
        description = data['weather'][0]['description'].capitalize()
        temperature = round(data['main']['temp'])  # Round temperature to nearest integer
        humidity = data['main']['humidity']
        return weather_condition, description, temperature, humidity
    else:
        return None

# Function to generate a weather summary
def generate_weather_summary(city, description, temperature, humidity):
    prompt = f"The weather in {city} is currently {description} with a temperature of {temperature}°C and humidity at {humidity}%. Provide a short summary and advisory for people."
    response = llm.invoke(prompt)
    return response.strip()

# Streamlit UI
st.set_page_config(page_title="City Weather Check", page_icon="🌤️", layout="centered")

st.sidebar.header("Enter City Name")
city = st.sidebar.text_input("City", placeholder="Enter city name...")

if city:
    if st.button("Check Weather"):
        with st.spinner("Fetching weather data..."):
            weather = get_weather(city)
            if weather:
                condition, description, temperature, humidity = weather
                summary = generate_weather_summary(city, description, temperature, humidity)
                
                # Select background color & icon based on weather condition
                background_color = WEATHER_BACKGROUNDS.get(condition, WEATHER_BACKGROUNDS["default"])
                weather_icon = WEATHER_ICONS.get(condition, WEATHER_ICONS["default"])

                # Apply custom background color
                st.markdown(f"""
                    <style>
                        .main {{
                            background-color: {background_color};
                            padding: 20px;
                            border-radius: 10px;
                        }}
                        .weather-box {{
                            text-align: center;
                            padding: 20px;
                            border-radius: 10px;
                            background-color: white;
                            width: 300px;
                            margin: auto;
                        }}
                        .temperature {{
                            font-size: 50px;
                            font-weight: bold;
                        }}
                        .icon {{
                            font-size: 80px;
                        }}
                    </style>
                    <div class="main">
                        <div class="weather-box">
                            <div class="icon">{weather_icon}</div>
                            <p class="temperature">{temperature}°C</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # Display weather details
                st.subheader(f"Weather in {city}")
                st.write(f"**Condition:** {description}")
                st.write(f"**Humidity:** {humidity}%")

                # Display AI-generated weather summary
                st.markdown("### AI Generated Summary")
                st.write(summary)
            else:
                st.error("City not found. Please enter a valid city name.")
