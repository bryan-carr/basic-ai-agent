# funtions/tools for the coding agent to use

import os

#New function -- get basic size and location info of files in a directory
def get_files_info(working_directory, directory=None):
    #if the directory is outside the working directory, return an error string

    #convert the working directory into an absolute path -- should be more reliable

    abs_path = os.path.abspath(working_directory)
    rel_path_target = os.path.join(working_directory, directory)
    target_dir_abs = os.path.abspath(rel_path_target)

    #error out if 'directory' argument is not a real directory
    if not os.path.isdir(target_dir_abs):
        return(f'Error: "{directory}" is not a directory')

    #list out the directories in our working dir
    dir_contents = os.listdir(abs_path)
    
    #build a list of sub-directories within the working directory
    list_of_abs_contents = []
    for d in dir_contents:
        temp_dir = os.path.join(abs_path, d)
        if os.path.isdir(temp_dir):
            list_of_abs_contents.append(temp_dir)


    #check if our target directory exists
    if (target_dir_abs not in list_of_abs_contents) and (directory != "."):
        return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')

    #list out contents of target directory
    target_contents = os.listdir(target_dir_abs)

    # try to generate an output. If this fails: return an Error message
    string_list = []
    try:
        for c in target_contents:
            temp_dir = os.path.join(target_dir_abs, c)
            try:
                size = os.path.getsize(temp_dir)
            except FileNotFoundError:
                size = 128
            string_rep = f"- {c}: file_size={size} bytes, is_dir={os.path.isdir(temp_dir)}"
            string_list.append(string_rep)
        
        #output the joined up string repreentations, one per line
        return "\n".join(string_list)
    except Exception as e:
        return f"Error: {str(e)}"

