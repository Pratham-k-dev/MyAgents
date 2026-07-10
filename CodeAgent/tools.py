from abc import ABC, abstractmethod
from pydantic import BaseModel


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