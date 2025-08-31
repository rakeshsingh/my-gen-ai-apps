from mcp.server import FastMCP
from geopy.geocoders import Nominatim
import requests
import json


mcp = FastMCP("Calculator Server")

@mcp.tool(description="Add two numbers together")
def add(x: int, y: int) -> int:
    """Add two numbers and return the result."""
    return x + y

@mcp.tool(description="Get the geographic location such as latitude and longitude of a given address or a city")
def get_geolocation_coordinates(address:str) -> dict:
    """Get the latitude and longitude of an address"""
    geolocator = Nominatim(user_agent="my_agent")
    location = geolocator.geocode(address)
    location_dict = {
        "address": location.address,
        "latitude": location.latitude,
        "longitude": location.longitude
    }
    return location_dict

@mcp.tool(description="Get the weekly and daily forecast for a given latitude and longiude")
def get_weather_by_coordinates(latitude:str, longitude:str):
    """
    Get weather data from NWS API using latitude and longitude coordinates.
    
    Args:
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
    
    Returns:
        dict: Weather data including current conditions and forecast
    """
    
    # Step 1: Get the grid point data for the coordinates
    points_url = f"https://api.weather.gov/points/{latitude},{longitude}"
    
    try:
        # Set user agent (required by NWS API)
        headers = {
            'User-Agent': 'WeatherApp/1.0 (kumar.rakesh@gmail.com)'
        }
        
        points_response = requests.get(points_url, headers=headers)
        points_response.raise_for_status()
        points_data = points_response.json()
        
        # Extract forecast URLs
        forecast_url = points_data['properties']['forecast']
        forecast_hourly_url = points_data['properties']['forecastHourly']
        
        # Step 2: Get the forecast data
        forecast_response = requests.get(forecast_url, headers=headers)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()
        
        # Step 3: Get hourly forecast (optional)
        hourly_response = requests.get(forecast_hourly_url, headers=headers)
        hourly_response.raise_for_status()
        hourly_data = hourly_response.json()
        
        return {
            'location': points_data['properties']['relativeLocation']['properties'],
            'forecast': forecast_data['properties']['periods'][:7],  # 7-day forecast
            'hourly': hourly_data['properties']['periods'][:12]      # 12-hour forecast
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    except KeyError as e:
        print(f"Error parsing weather data: {e}")
        return None

#run the mcp server
mcp.run(transport="streamable-http")


# if __name__ == "__main__":
#     # Example 1: Get weather by coordinates (Seattle)
#     print("Getting weather for Seattle, WA...")
#     location = get_geolocation_coordinates("Seattle, WA")
#     print("Location:", location['address'], location['latitude'], location['longitude'])
#     weather = get_weather_by_coordinates(location['latitude'], location['longitude'])
#     print(weather)