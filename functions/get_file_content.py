import os
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_working = os.path.abspath(working_directory)
    abs_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file.startswith(abs_working):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abs_file, "r") as f:
            content = f.read(10000)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at 10000 characters]'
            return content
    except Exception as e:
        return f'Error: {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the content of a file inside the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the file to read."
            )
        },
        required=["file_path"]
    )
)
