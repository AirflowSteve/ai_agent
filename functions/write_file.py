import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes text content to a specified file within the working directory (overwriting if the file exists)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Text content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}



def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(absolute_path, file_path))
        if os.path.isdir(full_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        common_path = os.path.commonpath([absolute_path, full_path])
        if common_path != absolute_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return f'Error: {e}'

    try:
        parent_dir = os.path.dirname(full_path)
        os.makedirs(parent_dir, exist_ok=True)
        with open(full_path, "w") as file:
            
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
    