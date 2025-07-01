#Call_Function -- a file to organize our funciton calls

from google.genai import types

from functions.get_file_content import schema_get_file_content, get_file_content
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

#Collect all functions in a list of Available Functions
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

#dict we use later on to look up our functions
function_lookup = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file
}

def call_function(function_call_part, verbose=False):
    #function_call_part is a tuple with .name and .args

    if verbose == True:
        print(f" - Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    #catch invalid function names and return an error
    if function_call_part.name not in function_lookup:
            return types.Content(
                 role="tool",
                 parts=[
                      types.Part.from_function_response(
                           name=function_call_part.name,
                           response={"error": f"Unknown function: {function_call_part.name}"}
                      )
                 ],
            )

    try:
        func = function_lookup[function_call_part.name]

        args = function_call_part.args
        args["working_directory"] = "./calculator"

        function_result = func(**args)

        return types.Content(
             role="tool",
             parts=[
                  types.Part.from_function_response(
                       name=function_call_part.name,
                       response={"result": function_result},
                  )
             ],
        )
    except Exception as e:
         print(f"Error calling function: {e}")
