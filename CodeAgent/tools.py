from abc import ABC, abstractmethod
from pydantic import BaseModel

import inspect
from typing import get_origin, get_args


class ToolResult(BaseModel):
    success: bool
    output: str

    def __str__(self):
        return self.output


class BaseTool(ABC):
    name: str
    description: str
    parameters: dict = {}

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        pass

    def to_prompt(self):
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }


class RunPythonTool(BaseTool):
    name = "run_python"
    description = "Execute a Python file inside the sandbox."

    parameters = {
        "type": "object",
        "properties": {
            "entry": {
                "type": "string",
                "description": "Python file to execute.",
                "default": "main.py",
            }
        },
        "required": [],
    }

    def __init__(self, workspace, sandbox):
        self.workspace = workspace
        self.sandbox = sandbox

    def execute(self, entry="main.py") -> ToolResult:
        result = self.sandbox.execute(
            self.workspace,
            entry
        )

        return ToolResult(
            success=result.exit_code == 0,
            output=result.output
        )


class WriteFileTool(BaseTool):
    name = "write_file"
    description = "Create or overwrite a file."

    parameters = {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Destination file path."
            },
            "content": {
                "type": "string",
                "description": "Content to write."
            }
        },
        "required": ["path", "content"]
    }

    def __init__(self, workspace):
        self.workspace = workspace

    def execute(self, path: str, content: str) -> ToolResult:
        self.workspace.write(path, content)

        return ToolResult(
            success=True,
            output=f"Successfully wrote '{path}'."
        )


class ReadFileTool(BaseTool):
    name = "read_file"
    description = "Read a file."

    parameters = {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "File path to read."
            }
        },
        "required": ["path"]
    }

    def __init__(self, workspace):
        self.workspace = workspace

    def execute(self, path: str) -> ToolResult:
        content = self.workspace.read(path)

        return ToolResult(
            success=True,
            output=content
        )


class AppendFileTool(BaseTool):
    name = "append_file"
    description = "Append content to a file."

    parameters = {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "File path."
            },
            "content": {
                "type": "string",
                "description": "Content to append."
            }
        },
        "required": ["path", "content"]
    }

    def __init__(self, workspace):
        self.workspace = workspace

    def execute(self, path: str, content: str) -> ToolResult:
        self.workspace.append(path, content)

        return ToolResult(
            success=True,
            output=f"Successfully appended to '{path}'."
        )


class DeleteFileTool(BaseTool):
    name = "delete_file"
    description = "Delete a file."

    parameters = {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "File to delete."
            }
        },
        "required": ["path"]
    }

    def __init__(self, workspace):
        self.workspace = workspace

    def execute(self, path: str) -> ToolResult:
        self.workspace.delete(path)

        return ToolResult(
            success=True,
            output=f"Successfully deleted '{path}'."
        )
    
class DecoratedTool(BaseTool):

    def __init__(self, func):
        self.func = func

        self.name = func.__name__
        self.description = inspect.getdoc(func) or ""

        self.signature = inspect.signature(func)

        self.parameters = self._build_schema()

    def execute(self, **kwargs) -> ToolResult:

        result = self.func(**kwargs)

        if isinstance(result, ToolResult):
            return result

        return ToolResult(
            success=True,
            output=str(result),
        )

    def _build_schema(self):

        properties = {}
        required = []

        for name, parameter in self.signature.parameters.items():

            annotation = parameter.annotation

            properties[name] = {
                "type": self._python_to_json(annotation),
                "description": f"{name} parameter"
            }

            if parameter.default is inspect.Parameter.empty:
                required.append(name)

        return {
            "type": "object",
            "properties": properties,
            "required": required,
        }

    def _python_to_json(self, annotation):

        mapping = {
            str: "string",
            int: "integer",
            float: "number",
            bool: "boolean",
            list: "array",
            dict: "object",
        }

        return mapping.get(annotation, "string")


def _tool(func):
    return DecoratedTool(func)