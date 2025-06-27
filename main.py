import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


from google import genai
import sys
from google.genai import types

#set up System Prompt -- instructions for the agent to follow
system_prompt = '''
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a funciton call plan. You can perform the following operations:
-List files and directories
-Read file contents
-Execute Python files without arguments
-Write or overwrite files

All paths you provide should be relative to the working directory. 
You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
'''

###Set up functions
#Function - Get_Files_Info - gets all files in the directory and their size
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

#Function -- get_file_content -- gets the content of a file, as a string
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

#Function -- write_file -- writes or overwrites a file
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

#Function -- run_python_file -- runs a python file within the directory
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file, with the Python 3 interpreter. Constrained to only run files within the working directory. No additional arguments are allowed - this is intended for testing code updates.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the python file to be run. Must be in the working directory. Must be a valid python file ending in .py.",
            ),
        },
    ),
)

###print("Function set up")

#Collect all functions in a list of Available Functions
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)
###print("Functions listed")

#read in user prompt
user_prompt = sys.argv[1]
if user_prompt is None or len(user_prompt) == 0:
    print("exit code 1")
    exit
###print("User prompt read in")

#initialize the Gemini Client for the agent
client = genai.Client(api_key = api_key)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

###print("Calling model to generate a response")
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(
        system_instruction = system_prompt,
        tools=[available_functions]             #give the list of functions as useable tools
        )
)

###print("Response in, generating output")
#get metadata from the response
prompt_token_count = response.usage_metadata.prompt_token_count
response_token_count = response.usage_metadata.candidates_token_count

#get function calls from the response
#function_call_part = response.function_calls[0]

#print the response and any functions to be called
print(response.text)
#print(function_call_part)
for f in response.function_calls:
    print(f"Calling function: {f.name}({f.args})")

# Make use of a "Verbose" tag to give the user more info
if "--verbose" in sys.argv:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_token_count}")
    print(f"Response tokens: {response_token_count}")