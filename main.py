from prompts import system_prompt
import os
import sys
from call_functions import available_functions, call_function
from google.genai import types
import argparse
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found")

    parser = argparse.ArgumentParser(description="AI Agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    verbose = args.verbose

    # ONLY USER MESSAGE
    message = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    client = genai.Client(api_key=api_key)

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0
            ),
        )

        for candidate in response.candidates:
            message.append(candidate.content)

        # List to store function results (Boot.dev requirement)
        function_results = []

        if response.function_calls:
            for function_call in response.function_calls:

                # 1. Call the function
                function_call_result = call_function(function_call, verbose=verbose)

                # 2. Validate .parts
                if not function_call_result.parts:
                    raise Exception("Function returned no parts")

                # 3. Extract function_response
                function_response = function_call_result.parts[0].function_response
                if function_response is None:
                    raise Exception("FunctionResponse is None")

                # 4. Extract .response (actual result)
                response_payload = function_response.response
                if response_payload is None:
                    raise Exception("FunctionResponse.response is None")

                # 5. Save the part for later (Boot.dev requirement)
                function_results.append(function_call_result.parts[0])

                message.append(types.Content(role="user", parts=function_results))

                # 6. Verbose output
                if verbose:
                    print(f"-> {response_payload}")

        else:
            print(response.text)
            return
    print("Se alcanzo el maximo de iteraciones (20) sin respuesta final")
    sys.exit(1)
    
if __name__ == "__main__":
    main()
