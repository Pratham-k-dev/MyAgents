# optimizer.py

from .schemas import Message
from pydantic import BaseModel, Field

class SummaryResponse(BaseModel):
    summary: str = Field(
        description="The updated long-term conversation summary."
    )


class Summarizer:

    SYSTEM_PROMPT = """
You maintain the long-term memory of an AI assistant.

Your task is to update the existing summary using the new conversation.

Rules:
- Preserve important long-term facts.
- Preserve user preferences.
- Preserve unfinished tasks.
- Preserve completed milestones.
- Remove repetitive details.
- Be concise.
- Do not invent information.

Return only the updated summary."""

    def summarize(
        self,
        model,
        previous_summary: str,
        messages: list[Message],
    ) -> str:

        conversation = "\n".join(
            f"{msg.role}: {msg.content}"
            for msg in messages
        )

        prompt = f"""
Current Summary:
{previous_summary}

New Conversation:
{conversation}

Update the summary."""
        msg=model.generate(
           messages=[
    {
        "role": "user",
        "parts": [
            {
                "text": self.SYSTEM_PROMPT
            }
        ]
    },
    {
        "role": "user",
        "parts": [
            {
                "text": prompt
            }
        ]
    },
],
            response_schema=SummaryResponse,
        )
        print("executing:  " +msg.summary)
        return msg.summary

class ContextOptimizer:

    def __init__(
        self,
        window_size: int = 30,
        summarize_threshold: int = 60,
    ):
        self.window_size = window_size
        self.summarize_threshold = summarize_threshold

    def should_optimize(
        self,
        messages: list[Message],
    ) -> bool:

        return len(messages) >= self.summarize_threshold

    def split_messages(
        self,
        messages: list[Message],
    ) -> tuple[list[Message], list[Message]]:

        if not self.should_optimize(messages):
            return [], messages

        summarize = messages[:-self.window_size]
        keep = messages[-self.window_size:]

        return summarize, keep
    