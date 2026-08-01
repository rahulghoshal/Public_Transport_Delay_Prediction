import streamlit as st
import pandas as pd
import joblib

# Load your trained model (update path if needed)
classifier_model = joblib.load("transport_delay_model.pkl")

st.title("🚍 Public Transport Delay Prediction")

st.write("Fill in the trip details below to predict whether the transport will be delayed.")

# User inputs
route_id = st.number_input("Route_ID", 0, 19)
origin_station = st.number_input("Origin Station", 0, 49)
destination_station = st.number_input("Destination Station", 0, 49)

actual_departure_delay_min = st.number_input("Departure Delay (minutes)", min_value=0, max_value=60, value=3)
actual_arrival_delay_min = st.number_input("Arrival Delay (minutes)", min_value=0, max_value=60, value=7)

temperature_C = st.number_input("Temperature (°C)", min_value=-10.0, max_value=40.0, value=18.5)
humidity_percent = st.slider("Humidity (%)", 0, 100, 78)
wind_speed_kmh = st.slider("Wind Speed (km/h)", 0, 100, 22)
precipitation_mm = st.number_input("Precipitation (mm)", min_value=0.0, max_value=50.0, value=5.2)

event_attendance_est = st.number_input("Event Attendance Estimate", min_value=0, max_value=50000, value=5000)
traffic_congestion_index = st.slider("Traffic Congestion Index", 0, 100, 65)

holiday = st.radio("Holiday?[0:Y/1:N]", [0, 1])
peak_hour = st.radio("Peak Hour?", [0, 1])
weekday = st.slider("Weekday (0=Mon … 6=Sun)", 0, 6, 6)

year = st.number_input("Year", min_value=2023, max_value=2030, value=2023)
month = st.slider("Month", 1, 12, 2)
day = st.slider("Day", 1, 31, 5)
hour = st.slider("Hour", 0, 23, 8)
minute = st.number_input("Enter Minute (0–59): ", min_value=0, max_value=59, value=30)
scheduled_departure_hour = st.number_input("Enter Scheduled Departure Hour (0–23): ", min_value=0, max_value=23, value=8)
scheduled_departure_minute = st.number_input("Enter Scheduled Departure Minute (0–59): ", min_value=0, max_value=59, value=30)
scheduled_arrival_hour = st.number_input("Enter Scheduled Arrival Hour (0–23): ", min_value=0, max_value=23, value=9)
scheduled_arrival_minute = st.number_input("Enter Scheduled Arrival Minute (0–59): ", min_value=0, max_value=59, value=30)

# Categorical inputs
transport_type = st.selectbox("Transport Type", ["Bus", "Train", "Tram", "Metro"])
weather_condition = st.selectbox("Weather Condition", ["Clear", "Cloudy", "Rain", "Snow", "Fog", "Storm"])
event_type = st.selectbox("Event Type", ["No Event", "Festival", "Sports", "Concert", "Parade", "Protest"])
season = st.selectbox("Season", ["Spring", "Summer", "Winter", "Autumn"])

# Build unseen row with one-hot encoding
unseen_row = pd.DataFrame([{
    "route_id": route_id,
    "origin_station": origin_station,
    "destination_station": destination_station,
    "actual_departure_delay_min": actual_departure_delay_min,
    "actual_arrival_delay_min": actual_arrival_delay_min,
    "temperature_C": temperature_C,
    "humidity_percent": humidity_percent,
    "wind_speed_kmh": wind_speed_kmh,
    "precipitation_mm": precipitation_mm,
    "event_attendance_est": event_attendance_est,
    "traffic_congestion_index": traffic_congestion_index,
    "holiday": holiday,
    "peak_hour": peak_hour,
    "weekday": weekday,
    "year": year,
    "month": month,
    "day": day,
    "hour": hour,

    # Transport type one-hot
    "transport_type_Metro": 1 if transport_type=="Metro" else 0,
    "transport_type_Train": 1 if transport_type=="Train" else 0,
    "transport_type_Tram": 1 if transport_type=="Tram" else 0,

    # Weather condition one-hot
    "weather_condition_Cloudy": 1 if weather_condition=="Cloudy" else 0,
    "weather_condition_Fog": 1 if weather_condition=="Fog" else 0,
    "weather_condition_Rain": 1 if weather_condition=="Rain" else 0,
    "weather_condition_Snow": 1 if weather_condition=="Snow" else 0,
    "weather_condition_Storm": 1 if weather_condition=="Storm" else 0,

    # Event type one-hot
    "event_type_Festival": 1 if event_type=="Festival" else 0,
    "event_type_No Event": 1 if event_type=="No Event" else 0,
    "event_type_Parade": 1 if event_type=="Parade" else 0,
    "event_type_Protest": 1 if event_type=="Protest" else 0,
    "event_type_Sports": 1 if event_type=="Sports" else 0,

    # Season one-hot
    "season_Spring": 1 if season=="Spring" else 0,
    "season_Summer": 1 if season=="Summer" else 0,
    "season_Winter": 1 if season=="Winter" else 0,

    # Time features
    "time_hour": hour,
    "time_minute": minute,
    "scheduled_departure_hour": scheduled_departure_hour,
    "scheduled_departure_minute": scheduled_departure_minute,
    "scheduled_arrival_hour": scheduled_arrival_hour,
    "scheduled_arrival_minute": scheduled_arrival_minute
}])

# Predict button
if st.button("Predict Delay or No Delay"):
    pred = classifier_model.predict(unseen_row)[0]
    if pred == 0:
        st.success("✅ Prediction: No Delay")
    else:
        st.error("⚠️ Prediction: Delay")

