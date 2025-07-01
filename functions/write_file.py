# New function -- Write a file out

import os
from google.genai import types

def write_file(working_directory, file_path, content):
    rel_path = os.path.join(working_directory, file_path)
    abs_path_base = os.path.abspath(working_directory)
    abs_path_target_file = os.path.abspath(rel_path)
    abs_target_directory_path = os.path.dirname(abs_path_target_file)    

    #if target file is not in the directory, return an Error string
    if not abs_path_target_file.startswith(abs_path_base):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    #create the directory if it does not exist
    try:
        if not os.path.exists(abs_target_directory_path):
            os.makedirs(abs_target_directory_path)
    except Exception as e:
        return f"Error creating directory: {e}"
    
    #write file out, overwriting any existing content
    try:
        with open(abs_path_target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'  #success message
    except Exception as e:
        return f"Error writing output: {e}"


#Function -- write_file -- writes or overwrites a file
#Defined here for our Call_Function file
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the provided content/string to a file. If a file already exists, it will be overwritten, so be sure to include all contents.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to be created or overwritten, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written into the file. Provide as a string, as you want it to appear. Do not include string formatting - only the content as you want it to appear in the file."
            )
        }
    )
)