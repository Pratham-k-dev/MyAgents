class BaseModel:

    def generate(
        self,
        messages,
        response_schema,
        tools=None,
        **kwargs
    ):
        raise NotImplementedError
    

import os
from typing import Type

from google import genai
from google.genai import types
from pydantic import BaseModel

from .base_model import BaseModelProvider


class GeminiModel(BaseModelProvider):

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gemini-2.5-flash",
        temperature: float = 0.0,
    ):
        self.client = genai.Client(
            api_key= api_key or os.getenv("GEMINI_API_KEY")
        )

        self.model = model
        self.temperature = temperature

    def generate(
        self,
        messages: list,
        response_schema: Type[BaseModel],
        **kwargs,
    ) -> BaseModel:

        response = self.client.models.generate_content(
            model=self.model,
            contents=messages,
            config=types.GenerateContentConfig(
                temperature=self.temperature,
                response_mime_type="application/json",
                response_schema=response_schema,
            ),
        )

        return response.parsed