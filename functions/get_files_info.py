import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(absolute_path, directory))
        if not os.path.isdir(full_path):
            
            return f'Error: "{directory}" is not a directory'
        common_path = os.path.commonpath([absolute_path, full_path])
        if common_path != absolute_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except Exception as e:
        return f'Error: {e}'

    try:
        directories = os.listdir(full_path)
        
        dirs_info = []
        for dir in directories:
            size = os.path.getsize(os.path.join(full_path, dir))
            is_dir = os.path.isdir(os.path.join(full_path, dir))
            dirs_info.append(f" - {dir}: file_size={size} byte, is_dir={is_dir}")

        return "\n".join(dirs_info)
    except Exception as e:
        return f"Error: {e}"
