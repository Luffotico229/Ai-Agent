from functions.get_files_info import get_files_info, schema_get_files_info
from functions.write_file import write_file, schema_write_file
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from google.genai import types

# Funciones reales que se ejecutan en tu máquina
real_functions = {
    "get_files_info": get_files_info,
    "write_file": write_file,
    "run_python_file": run_python_file,
    "get_file_content": get_file_content,
}

def call_function(function_call, verbose=False):
    func_name = function_call.name or ""
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"

    if verbose:
        print(f"Calling function: {func_name}({args})")
    else:
        print(f" - Calling function: {func_name}")

    if func_name not in real_functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"Unknown function: {func_name}"},
                )
            ]
        )

    func = real_functions[func_name]
    function_result = func(**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"result": function_result},
            )
        ],
    )

# ---------------------------------------------------------
# ESTA ES LA PARTE QUE TE FALTABA
# ---------------------------------------------------------

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_get_file_content,
        schema_run_python_file,
    ]
)
