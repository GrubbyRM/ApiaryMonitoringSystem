import requests
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime, timezone

# Firebase credentials
cred = credentials.Certificate("ApiaryMonitoringSystem/config/firebase-credentials.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://apiary-monitoring-system-default-rtdb.europe-west1.firebasedatabase.app/"
})

# Wadowice
latitude = 49.8837
longitude = 19.4930

def fetch_weather():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    current = data["current_weather"]
    return {
        "temperature": current["temperature"],
        "windspeed": current["windspeed"],
        "weather_code": current["weathercode"]
    }

def push_to_firebase(weather_data):
    print(weather_data)
    ref_now = db.reference("/weather/now")
    ref_now.set({
        "temperature": weather_data["temperature"],
        "windspeed": weather_data["windspeed"],
        "weather_code": weather_data["weather_code"]
    })
    timestamp = generate_date()
    ref_history = db.reference(f"/weather/history/{timestamp}")
    ref_history.set({
        "temperature": weather_data["temperature"],
        "windspeed": weather_data["windspeed"],
        "weather_code": weather_data["weather_code"]
    })

def generate_date():
    now = datetime.now()
    date_str = now.strftime("%d-%m-%Y")
    
    hour = now.hour
    if hour < 11:
        reading_id = "01"
    elif hour < 16:
        reading_id = "02"
    else:
        reading_id = "03"

    key = f"{date_str}-{reading_id}"
    return key

if __name__ == "__main__":
    pogoda = fetch_weather()
    push_to_firebase(pogoda)
