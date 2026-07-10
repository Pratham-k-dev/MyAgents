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


def streamlit_callback(event: AgentEvent,st):

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