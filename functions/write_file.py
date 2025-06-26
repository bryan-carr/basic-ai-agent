# New function -- Write a file out

import os

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