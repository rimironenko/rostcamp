from openai import OpenAI
from app.config import OPENAI_API_KEY, MODEL_NAME, DEFAULT_TEMPERATURE, MAX_TOKENS

class LLMClient:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = MODEL_NAME
        self.temperature = DEFAULT_TEMPERATURE
        self.max_tokens = MAX_TOKENS

    def get_completion(self, prompt: str) -> str:
        """
        Send a prompt to OpenAI and get the completion.
        
        Args:
            prompt (str): The prompt to send to the model
            
        Returns:
            str: The model's response
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error getting completion from OpenAI: {str(e)}")
