import os
import subprocess
from google.genai import types   # <-- ESTE IMPORT FALTABA

def run_python_file(working_directory, file_path, args=None):
    abs_working = os.path.abspath(working_directory)
    abs_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file.startswith(abs_working):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    
    try:
        command = ["python", abs_file]

        if args is not None:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=abs_working,
            capture_output=True,
            text=True,
            timeout=30
        )

        output = ""

        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"

        if not result.stdout and not result.stderr:
            output += "No output produced\n"

        if result.stdout:
            output += f"STDOUT: {result.stdout}\n"

        if result.stderr:
            output += f"STDERR: {result.stderr}\n"

        return output

    except Exception as e:
        return f"Error: excecuting Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file inside the working directory and return its stdout.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the Python file to execute."
            )
        },
        required=["file_path"]
    )
)
