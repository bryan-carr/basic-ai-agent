import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from call_function import available_functions, call_function
from config import system_prompt, MAX_STEPS



def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    #initialize the Gemini Client for the agent
    client = genai.Client(api_key = api_key)

    # Check if "Verbose" tag was used
    verbose = "--verbose" in sys.argv

    #read in user prompt
    user_prompt = sys.argv[1]
    if user_prompt is None or len(user_prompt) == 0:
        print("exit code 1 -- No prompt detected! Must enter a prompt with length > 0")
        exit

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    if verbose:
        print(f"User prompt: {user_prompt}")

    #generate responses for up to MAX_STEPS number of steps. Default max is 20.
    iter_count = 0
    while True:
        iter_count += 1

        print(f"Running iteration # {iter_count}")

        #if 20 iters: stop
        if iter_count > MAX_STEPS:
            print(f"Maximum number of function call steps reached ({MAX_STEPS})")
            sys.exit(1)
        
        try:
            response = generate_content(client, messages, verbose)
            if response:
                print("FINAL RESPONSE:")
                print(response)
                break
        except Exception as e:
            print(f"Error in generate_content function: {e}")
            break
    

def generate_content(client, messages, verbose):
    #call the model with the Message history, to generate the next possible response
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction = system_prompt,
                tools=[available_functions]             #give the list of functions as useable tools
                )
        )
    except Exception as e:
        print(f"Error in creating a Response, calling the model: {e}")

    # append the Candidate response to Messages, as an answer from the Model (Role = "Model")
    if response.candidates is not None:
        for candidate in response.candidates:   # candidate is it  "Candidate" object below
            # candidate.content is the Content we see below -- this is what we want to append to Messages to track and continue the agent's outputs (the 'conversation' between itself and the functions/tools)
            messages.append(candidate.content)

    #print(response)

    """
    Inspecting a Candidate response object:

    [Candidate(
        content=Content(
            parts=[
                Part(video_metadata=None, 
                    thought=None, 
                    code_execution_result=None, 
                    executable_code=None, 
                    file_data=None, 
                    function_call=FunctionCall(id=None, args={'directory': '.'}, name='get_files_info'), 
                    function_response=None, 
                    inline_data=None, text=None
                )
            ], 
            role='model'
        ), 
        citation_metadata=None, 
        finish_message=None, 
        token_count=None, 
        finish_reason=<FinishReason.STOP: 'STOP'>, 
        avg_logprobs=-0.03558335346835, 
        grounding_metadata=None, 
        index=None, 
        logprobs_result=None, 
        safety_ratings=None)
    ]
    """

    #get metadata from the response
    prompt_token_count = response.usage_metadata.prompt_token_count
    response_token_count = response.usage_metadata.candidates_token_count

    # Make use of a "Verbose" tag to give the user more info
    if verbose:
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {response_token_count}")

    #print("CHECKING AND PRINTING MESSAGE HISTORY")
    #for m in messages:
    #    print(m)

    #if the function response has no further calls, then return the text
    if not response.function_calls:
        return response.text

    #Call the function!!
    function_responses = []
    for f in response.function_calls:
        # if no functions are called - break the cycle and return the last response
        print(f"Calling function: {f.name}({f.args})")
        function_call_result = call_function(f, verbose)

        #append the Function Call Result to the Messages - to track the result in the 'conversation' history
        # this addition has the Role="Tool"
        if function_call_result is not None:
            messages.append(function_call_result)
        else:
            print("Function call result is NONE, not appending")


        if (len(function_call_result.parts) == 0) or (not hasattr(function_call_result.parts[0].function_response, "response")):
            raise Exception("Fatal error: function resposne did not return in format: function_call_result.parts[0].function_response.response")
        
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])
        
    if not function_responses:
        raise Exception("no function responses generated, exiting")
    
    #return function_responses

if __name__ == "__main__":
    main()
