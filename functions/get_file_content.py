import os

from config import *

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": f"Retrieves the content (at most {MAX_CHARS_READING} characters) of a specified file within the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}






def get_file_content(working_directory: str, file_path: str ) -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(absolute_path, file_path))
        if not os.path.isfile(full_path):
                
            return f'Error: File not found or is not a regular file: "{file_path}"'
        common_path = os.path.commonpath([absolute_path, full_path])
        if common_path != absolute_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return f'Error: {e}'
    try:
        with open(full_path) as file:
            file_content = file.read(MAX_CHARS_READING)
            if file.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS_READING} characters]'

        return file_content
    except Exception as e:
        return f"Error: {e}"