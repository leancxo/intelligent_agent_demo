# tools/weather_tool.py
import os
import requests
from langchain.tools import Tool


class WeatherTool:
    """Tool for retrieving current weather information for locations."""

    def __init__(self):
        """Initialize the weather API client."""
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, location):
        """
        Get current weather for a location.

        Args:
            location (str): City name or location

        Returns:
            str: Weather information
        """
        try:
            # Make API request
            params = {
                "q": location,
                "appid": self.api_key,
                "units": "metric"  # Use Celsius
            }
            response = requests.get(self.base_url, params=params)
            data = response.json()

            if response.status_code == 200:
                # Format the weather information
                weather_desc = data["weather"][0]["description"]
                temp = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"]

                return (
                    f"Weather in {location}:\n"
                    f"- Condition: {weather_desc}\n"
                    f"- Temperature: {temp}°C\n"
                    f"- Humidity: {humidity}%\n"
                    f"- Wind Speed: {wind_speed} m/s"
                )
            else:
                return f"Error getting weather: {data.get('message', 'Unknown error')}"

        except Exception as e:
            return f"Failed to get weather information: {str(e)}"

    def get_tool(self):
        """Return the tool object for the agent to use."""
        return Tool(
            name="WeatherLookup",
            func=self.get_weather,
            description="Useful for when you need to find weather information for a location. Input should be a city name."
        )