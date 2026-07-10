ROLE_MAP = {
    "assistant": "model",
    "user": "user",
    "tool": "user",
    "system": "user",
}

# context.py

from .schemas import Message

class BaseContextBuilder:

    def build(
        self,
        system_prompt: str,
        summary: str,
        messages: list[Message],
    ):
        raise NotImplementedError


class GeminiContextBuilder(BaseContextBuilder):

    ROLE_MAP = {
        "user": "user",
        "assistant": "model",
        "tool": "user",
        "system": "user",
    }

    def build(
        self,
        system_prompt: str,
        summary: str,
        messages: list[Message],
    ) -> list[dict]:

        context = []

        # System Prompt
        context.append({
            "role": "user",
            "parts": [
                {
                    "text": system_prompt
                }
            ]
        })

        # Conversation Summary
        if summary.strip():
            context.append({
                "role": "user",
                "parts": [
                    {
                        "text": f"Conversation Summary:\n{summary}"
                    }
                ]
            })

        # Conversation History
        for msg in messages:

            role = self.ROLE_MAP.get(msg.role, "user")

            context.append({
                "role": role,
                "parts": [
                    {
                        "text": msg.content
                    }
                ]
            })

        return context