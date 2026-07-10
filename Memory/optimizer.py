# optimizer.py

from .schemas import Message


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