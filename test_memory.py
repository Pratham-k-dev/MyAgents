"""
test_memory.py

This script tests the complete memory subsystem.

Flow:
1. Create a new ConversationMemory.
2. Insert enough messages to exceed the optimization threshold.
3. Print database state BEFORE optimization.
4. Run optimize().
5. Print database state AFTER optimization.

Expected:
- Summary is generated.
- Old messages are deleted.
- Recent window is kept.
"""

from Memory.memory import ConversationMemory
from Memory.store import SQLiteStore
from Memory.optimizer import ContextOptimizer, Summarizer
from Memory.context import ContextBuilder
from CodeAgent.llms.gemini_model import GeminiModel
from dotenv import load_dotenv
import uuid

load_dotenv()

# -------------------------------
# Configure model
# -------------------------------

model = GeminiModel(
    api_key="GEMINI_API_KEY",
    model="gemini-2.5-flash",
)

# -------------------------------
# Create memory
# -------------------------------
builder = ContextBuilder()

optimizer = ContextOptimizer(
    window_size=30,
    summarize_threshold=60,
)
store=SQLiteStore("memory.db")
summarizer=Summarizer()

memory = ConversationMemory(
    store=store,
    builder=builder,
    optimizer=optimizer,
    summarizer=summarizer,
    
    session_id="my_id"
)

# -------------------------------
# Insert dummy conversation
# -------------------------------

# We intentionally exceed the optimizer threshold.
# If threshold = 60 and window = 30,
# optimization should summarize ~40 messages.

for i in range(70):

    if i % 2 == 0:
        role = "user"
    else:
        role = "assistant"

    memory.add_user_message(
        f"This is dummy message number {i}"
    )

# -------------------------------
# BEFORE optimization
# -------------------------------

# print("=" * 60)
# print("BEFORE OPTIMIZATION")
# print("=" * 60)

# print("\nSummary:")
# print(memory.get_summary())

# messages = memory.get_messages()

# print(f"\nMessage Count: {len(messages)}")

# for m in messages:
#     print(m.__dict__)

# # -------------------------------
# # Run optimizer
# # -------------------------------

# print("\nRunning optimizer...\n")

# ss=memory.optimize(model,previous_summary="some",messages=messages)
# # ss=summarizer.summarize(model,previous_summary="nothing here summarze dumb things too ",messages=messages)
# print(ss)

# # -------------------------------
# # AFTER optimization
# # -------------------------------

# print("=" * 60)
# print("AFTER OPTIMIZATION")
# print("=" * 60)

# print("\nSummary:")
# print(memory.get_summary())

# messages = memory.get_messages()

# print(f"\nRemaining Messages: {len(messages)}")

# for m in messages:
#     print(m)

# print("\nTest Complete.")