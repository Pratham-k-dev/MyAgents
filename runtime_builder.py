import inspect
from tools import _tool
from Docker.sandbox import Workspace
class RuntimeBuilder:

    def __init__(self, workspace):
        self.workspace = workspace

    def build(self, tools):
        code = []

        # Dispatcher (mock for now)
        code.append(self._dispatcher())

        # Generate one wrapper per tool
        for tool in tools:
            code.append(self._wrapper(tool))

        self.workspace.write(
            "runtime.py",
            "\n\n".join(code)
        )

    def _dispatcher(self):
        return """
def __tool_call__(tool_name, **kwargs):
    raise NotImplementedError("Dispatcher not implemented yet.")
""".strip()

    def _wrapper(self, tool):

        sig = inspect.signature(tool.func)

        args = ", ".join(sig.parameters.keys())

        kwargs = ", ".join(
            f"{name}={name}"
            for name in sig.parameters.keys()
        )

        return f"""
def {tool.name}({args}):
    return __tool_call__(
        "{tool.name}",
        {kwargs}
    )
""".strip()
    
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


workspace=Workspace("CodeAgent/Docker/WorkSpace")
rb=RuntimeBuilder(workspace)
rb.build([weather])