from typing import Any, Dict, Literal, Optional, Union
from pydantic import BaseModel, Field,ConfigDict






class ToolCall(BaseModel):
    """Represents an action where the agent wants to execute a tool."""
    

    type: Literal["tool"] = "tool"

    thought: str = Field(
        description="Reasoning behind choosing the tool."
    )

    tool: str = Field(
        description="Name of the tool to execute."
    )

    arguments: str


class FinalAnswer(BaseModel):
    """Represents the final response to the user."""
    

    type: Literal["final"] = "final"

    thought: str = Field(
        description="Reasoning before returning the final answer."
    )

    final_answer: str = Field(
        description="Final response for the user."
    )


class AgentAction(BaseModel):
    type: Literal["tool", "final"]

    thought: str

    tool: str | None = None
    arguments: str | None = None

    final_answer: str | None = None


class ToolResult(BaseModel):
    """Standardized result returned by every tool."""

    success: bool = Field(
        description="Whether the tool executed successfully."
    )

    output: str = Field(
        description="Output or error message from the tool."
    )

    metadata: str


class CodeGeneration(BaseModel):
    """Represents generated executable Python code."""

    type: Literal["code"] = "code"

    thought: str = Field(
        description="Reasoning behind the generated code."
    )

    code: str = Field(
        description="Executable Python code to be written into runtime.py."
    )

class CodeAgentAction(BaseModel):

    type: Literal["code", "final"]

    thought: str

    code: str | None = None

    final_answer: str | None = None