from Code_Agent import CodeAgent
from llms.gemini_model import GeminiModel
from tools import BaseTool, ToolResult
from dotenv import load_dotenv
from tools import WriteFileTool,_tool
from Docker.sandbox import Workspace
import streamlit as st
from toolModes import weather, calculator


load_dotenv()

from dataclasses import dataclass
from typing import Any, Callable, Optional
from enum import Enum
class EventType(str, Enum):
    THOUGHT = "thought"
    TOOL_CALL = "tool_call"
    OBSERVATION = "observation"
    FINAL_ANSWER = "final_answer"
    ERROR = "error"


@dataclass
class AgentEvent:
    type: EventType
    data: Any

def streamlit_callback(event: AgentEvent):

    if event.type == EventType.THOUGHT:
        st.info(f"💭 {event.data}")

    elif event.type == EventType.TOOL_CALL:
        st.warning(f"🔧 {event.data['tool']}")
        st.json(event.data["arguments"])

    elif event.type == EventType.OBSERVATION:
        st.success("📥 Observation")
        st.code(str(event.data))

    elif event.type == EventType.FINAL_ANSWER:
        st.chat_message("assistant").write(event.data)

    elif event.type == EventType.ERROR:
        st.error(event.data)

# class WeatherTool(BaseTool):
#     name = "get_weather"
#     description = "Returns the current weather for a city."

#     parameters = {
#         "type": "object",
#         "properties": {
#             "city": {
#                 "type": "string",
#                 "description": "Name of the city."
#             }
#         },
#         "required": ["city"]
#     }

#     def execute(self, city: str):
#         # Mock implementation
#         weather = {
#             "Delhi": "34°C, Sunny",
#             "Mumbai": "29°C, Rainy",
#             "Pune": "27°C, Cloudy"
#         }

#         return ToolResult(
#             success=True,
#             output=weather.get(city, f"No weather data available for {city}.")
#         )
# @_tool
# def weather(city: str) -> str:
#     """
#     Returns the current weather for a city.
#     This is a dummy implementation for testing the tool system.
#     """

#     weather_data = {
#         "mumbai": "30°C, Humid",
#         "delhi": "36°C, Sunny",
#         "pune": "26°C, Cloudy",
#         "bangalore": "24°C, Light Rain",
#         "hyderabad": "32°C, Clear",
#         "kolkata": "31°C, Thunderstorms",
#         "chennai": "33°C, Hot",
#     }

#     return weather_data.get(
#         city.lower(),
#         f"Weather data for '{city}' is unavailable."
#     )


model = GeminiModel(
    api_key="",
    model="gemma-4-26b-a4b-it"

)

agent = CodeAgent(
    model=model,
    tools=[
        weather,
        calculator
    ],
    cli_stream=True,
    tool_paths=["C:\\web dev\\AI\\Agent-Framework\\toolModes.py"],
)

response = agent.run(
    """
    What is (17 × 23) + (144 ÷ 12)? answer using the tools only not direct python code
    """
)

print(response)
# workspace=Workspace("./CodeAgent/Docker/Workspace")
# tool = WriteFileTool(workspace)
# tool.execute(**{"path": "code.py", "content": "def fibonacci(n):\n a, b = 0, 1\n for _ in range(n):\n print(a, end=\" \")\n a, b = b, a + b\n print()\n\nif __name__ == \"__main__\":\n fibonacci(10)"} )



# st.title("CodeAgent Demo")

# task = st.text_area(                                                    
#     "Task",
#     "What's the weather in Pune and Hyderabad?"
# )

# if st.button("Run Agent"):

#     agent = CodeAgent(
#         model=model,
#         tools=[weather],
#         tool_paths=[],
#         callback=streamlit_callback
#     )

#     response = agent.run(task)
#     st.write(response)
