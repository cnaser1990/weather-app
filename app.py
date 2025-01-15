import tkinter as tk
from tkinter import messagebox
import requests
from tkinter import PhotoImage


API_KEY = "640f5d47bf27456a163cd6f31020573c"

def get_weather(city):
    """Fetch weather data for the given city from Weatherstack."""
    url = f"http://api.weatherstack.com/current?access_key={API_KEY}&query={city}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        return weather_data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def display_weather():
    """Handle the button click to display the weather."""
    city = city_entry.get()
    if not city.strip():
        messagebox.showerror("Input Error", "Please enter a city name.")
        return

    result = get_weather(city)
    if "error" in result:
        messagebox.showerror("Error", f"Failed to fetch weather data: {result['error']}")
        return

    if "current" not in result:
        messagebox.showerror("Error", "City not found.")
        return

    location = result["location"]["name"]
    country = result["location"]["country"]
    temperature = result["current"]["temperature"]
    condition = result["current"]["weather_descriptions"][0]
    wind_speed = result["current"].get("windspeed", "N/A")
    humidity = result["current"]["humidity"]

    weather_output = (
        f"Weather in {location}, {country}:\n"
        f"Temperature: {temperature}°C\n"
        f"Condition: {condition}\n"
        f"Humidity: {humidity}%\n"
        f"Wind Speed: {wind_speed} km/h"
    )

    weather_label.config(text=weather_output, fg="#f5f5f5", bg="#4a90e2")

# Create the main Tkinter window
root = tk.Tk()
root.title("Weather App")
root.geometry("400x400")
root.resizable(False, False)
root.configure(bg="#4a90e2")

# Title Label
title_label = tk.Label(root, text="Weather App", font=("Arial", 20, "bold"), fg="#f5f5f5", bg="#4a90e2")
title_label.pack(pady=10)

# City Input Label and Entry
tk.Label(root, text="Enter City Name:", font=("Arial", 14), fg="#f5f5f5", bg="#4a90e2").pack(pady=5)
city_entry = tk.Entry(root, font=("Arial", 14), width=20, relief="solid", bd=2)
city_entry.pack(pady=5)

# Get Weather Button
tk.Button(root, text="Get Weather", font=("Arial", 14), bg="#f5a623", fg="#fff", relief="raised", command=display_weather).pack(pady=10)

# Weather Output Label
weather_label = tk.Label(root, font=("Arial", 12), justify="left", wraplength=350, bg="#4a90e2", fg="#f5f5f5")
weather_label.pack(pady=30)

# Run the main event loop
root.mainloop()