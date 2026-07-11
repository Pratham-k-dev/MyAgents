import docker

class DockerSandbox:
    def __init__(self):
        self.client = docker.from_env()

    def execute(self, workspace, entry):
        container = self.client.containers.run(
            image="python:3.12-slim",
            command=f"python {entry}",
            working_dir="/Workspace",
            volumes={
                str(workspace.root): {
                    "bind": "/Workspace",
                    "mode": "rw",
                }
            },
            detach=True,
            remove=False,
        )

        result = container.wait()

        logs = container.logs().decode()

        container.remove()

        return {
            "exit_code": result["StatusCode"],
            "output": logs,
        }


# sandbox = DockerSandbox()

# print(sandbox.client.containers.list())


# output = sandbox.client.containers.run(
#     image="python:3.12-slim",
#     command="python -c \"print('Hello from Docker')\"",
#     remove=True
# )

# print(output.decode())


from pathlib import Path


class Workspace:
    def __init__(self, root: str):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _resolve(self, path: str) -> Path:
        file = (self.root / path).resolve()

        # Prevent escaping the workspace
        if not str(file).startswith(str(self.root)):
            raise ValueError("Path outside workspace")

        return file

    def write(self, path: str, content: str):
        file = self._resolve(path)
        file.parent.mkdir(parents=True, exist_ok=True)

        with open(file, "w", encoding="utf-8") as f:
            f.write(content)

    def read(self, path: str) -> str:
        file = self._resolve(path)

        with open(file, "r", encoding="utf-8") as f:
            return f.read()

    def append(self, path: str, content: str):
        file = self._resolve(path)
        file.parent.mkdir(parents=True, exist_ok=True)

        with open(file, "a", encoding="utf-8") as f:
            f.write(content)

    def delete(self, path: str):
        file = self._resolve(path)
        file.unlink()

    def exists(self, path: str) -> bool:
        return self._resolve(path).exists()

    def list_files(self):
        return [
            str(f.relative_to(self.root))
            for f in self.root.rglob("*")
            if f.is_file()
        ]




# workspace.write("main.py", "print('Hello')")
# print(workspace.list_files())

# result = sandbox.execute(workspace, "main.py")

# print(result)

# sandbox=DockerSandbox()
# workspace= Workspace("./CodeAgent/Docker/WorkSpace")
# result = sandbox.execute(workspace, "main.py")

# print(result)