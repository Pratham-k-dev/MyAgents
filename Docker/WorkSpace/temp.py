
@_tool
def weather(city: str) -> str:
    """
    Returns the current weather for a city.
    This is a dummy implementation for testing the tool system.
    """

    weather_data = {
        "mumbai": "30°C, Humid",
        "delhi": "36°C, Sunny",
        "pune": "26°C, Cloudy",
        "bangalore": "24°C, Light Rain",
        "hyderabad": "32°C, Clear",
        "kolkata": "31°C, Thunderstorms",
        "chennai": "33°C, Hot",
    }

    return weather_data.get(
        city.lower(),
        f"Weather data for '{city}' is unavailable."
    )