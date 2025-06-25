import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


from google import genai
import sys
from google.genai import types

user_prompt = sys.argv[1]
if user_prompt is None or len(user_prompt) == 0:
    print("exit code 1")
    exit


client = genai.Client(api_key = api_key)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
)

prompt_token_count = response.usage_metadata.prompt_token_count
response_token_count = response.usage_metadata.candidates_token_count

print(response.text)

# Make use of a "Verbose" tag to give the user more info
if "--verbose" in sys.argv:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_token_count}")
    print(f"Response tokens: {response_token_count}")