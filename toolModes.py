from tools import _tool
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

from CodeAgent.tools import _tool


@_tool
def calculator(a: float, b: float, operation: str):
    """Perform a basic arithmetic operation.
    Args:
        a: First operand.
        b: Second operand.
        operation: One of '+', '-', '*', '/'.
    Returns number/ valueError
    """

    if operation == "+":
        return a + b

    if operation == "-":
        return a - b

    if operation == "*":
        return a * b

    if operation == "/":
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b

    raise ValueError(f"Unsupported operation: {operation}")

