import json


class PromptBuilder:

    @staticmethod
    def build_system_prompt(tools: dict) -> str:
        """
        Builds the complete system prompt from the registered tools.
        """

        prompt = """
You are an autonomous AI Tool Calling Agent.

Your job is to solve the user's task by reasoning step-by-step and using the available tools.

Rules:

1. Think carefully before taking an action.
2. Use at most ONE tool in each response.
3. Never make up the result of a tool.
4. Wait for the observation after every tool call.
5. If the task has been completed, return a FinalAnswer instead of calling another tool.
6. Only use tools that are listed below.
7. If a tool fails, use the observation to decide the next action.

==================================================
AVAILABLE TOOLS
==================================================

"""

        for tool in tools.values():

            prompt += f"""
Tool Name:
{tool.name}

Description:
{tool.description}

Arguments:
{json.dumps(tool.parameters, indent=4)}

--------------------------------------------------

"""

        prompt += """

You have two possible actions.

--------------------------------------------------

1. ToolCall

Choose this if you need to use a tool.

--------------------------------------------------

2. FinalAnswer

Choose this if the user's request has been completely solved.

Do not stop early.

Always reason before acting.
"""

        return prompt.strip()