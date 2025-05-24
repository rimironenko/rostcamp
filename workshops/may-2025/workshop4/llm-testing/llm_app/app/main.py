import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from .prompt_router import route_prompt
from .llm_client import LLMClient

def main():
    user_prompt = input("Enter your prompt: ")
    routed_prompt = route_prompt(user_prompt)
    client = LLMClient()
    response = client.get_completion(routed_prompt)
    print("\nLLM Response:")
    print(response)

if __name__ == "__main__":
    main()
