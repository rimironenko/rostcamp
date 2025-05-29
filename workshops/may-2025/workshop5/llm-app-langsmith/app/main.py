import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from .prompt_router import route_prompt
from .llm_client import LLMClient

def get_user_rating() -> int:
    """Get user rating for the response."""
    while True:
        try:
            rating = int(input("\nRate the response (1-5, where 5 is best): "))
            if 1 <= rating <= 5:
                return rating
            print("Please enter a number between 1 and 5")
        except ValueError:
            print("Please enter a valid number")

def get_user_feedback() -> str:
    """Get additional feedback from the user."""
    feedback = input("\nAdditional feedback (press Enter to skip): ").strip()
    return feedback if feedback else None

def main():
    # Initialize LLM client with a session ID
    llm_client = LLMClient()
    
    print("Welcome to the LLM Chat Application!")
    print("Type 'exit' to quit, or 'feedback' to see your feedback summary")
    
    # Get user input
    prompt = input("\nEnter your prompt: ").strip()
    
    if prompt.lower() == 'exit':
        print("\nGoodbye!")
        return
    elif prompt.lower() == 'feedback':
        feedback_summary = llm_client.get_feedback_summary()
        print("\nFeedback Summary:")
        for key, value in feedback_summary.items():
            print(f"{key}: {value}")
        return
    
    # Get completion from LLM
    try:
        response = llm_client.get_completion(prompt)
        print("\nLLM Response:")
        print(response)
        
        # Collect feedback
        rating = get_user_rating()
        feedback_text = get_user_feedback()
        
        # Store feedback
        llm_client.collect_feedback(
            prompt=prompt,
            response=response,
            rating=rating,
            feedback_text=feedback_text
        )
        
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
