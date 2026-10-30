import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes (or runs) a specified Python file within the working directory and returns its output, used specifically when the user asks to run a .py file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python script",
                },
            },
            "required": ["file_path"],
        },
    },
}



def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(absolute_path, file_path))
        if not os.path.isfile(full_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        common_path = os.path.commonpath([absolute_path, full_path])
        if common_path != absolute_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return f'Error: {e}'

    try:
        command = ["python", full_path]
        if args:
            command.extend(args)

        process = subprocess.run(command, cwd=absolute_path, capture_output=True, text=True, timeout=30)
        output = []
        if process.returncode != 0:
            output.append(f" - Process exited with code {process.returncode}") 
        if process.stderr == "" and process.stdout == "":
            output.append(" - No output produced")
        else:
            output.append(f"STDOUT: {process.stdout}")
            output.append(f"STDERR: {process.stderr}")
        output_string = "\n".join(output)
        return output_string
    except Exception as e:
        return f"Error: executing Python file: {e}"