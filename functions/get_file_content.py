#New function -- Read a file in, as a string

import os
from google.genai import types
MAXCHARS = 10000

def get_file_content(working_directory, file_path):

    rel_path = os.path.join(working_directory, file_path)
    abs_path_base = os.path.abspath(working_directory)
    abs_path_target = os.path.abspath(rel_path)

    #if target file is not a real file, return an Error string
    if not os.path.isfile(abs_path_target):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    #if target file is not in the directory, return an Error string
    print(f"target path: {abs_path_target}")
    if not abs_path_target.startswith(abs_path_base):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    try:
        #read in the file
        with open(abs_path_target, "r") as f:
            file_content_string = f.read(MAXCHARS)
        
        # add warning when Truncated to the max length of 10k
        if len(file_content_string) == 10000:
            file_content_string += f'''[...File "{file_path}" truncated at 10000 characters]'''

        return file_content_string
    except Exception as e:
        return f"Error reading file: {e}"
    

#Function Schema -- makes this function useable by the Gemini agent
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the contents of a file, as a string. Files are constrained to be within the working directory, or a subdirectory thereof.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the desired file, relative to the working directory.",
            ),
        },
    ),
)