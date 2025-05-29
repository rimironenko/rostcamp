from langchain_openai import ChatOpenAI
from langchain.callbacks import LangChainTracer
from openai import OpenAI
from langsmith import Client
import uuid
from typing import Optional
from .config import OPENAI_API_KEY, MODEL_NAME, DEFAULT_TEMPERATURE, MAX_TOKENS, LANGSMITH_API_KEY

class LLMClient:
    def __init__(self, session_id: Optional[str] = None, user_id: Optional[str] = None):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        # Just initialize the LangSmith client to verify API key works
        self.langsmith_client = Client(api_key=LANGSMITH_API_KEY)
        self.model = MODEL_NAME
        self.temperature = DEFAULT_TEMPERATURE
        self.max_tokens = MAX_TOKENS
        self.session_id = session_id or str(uuid.uuid4())
        self.user_id = user_id
        # LangChain LLM for tracing
        self.lc_llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        self.tracer = LangChainTracer()

    def get_completion(self, prompt: str) -> str:
        """
        Send a prompt to OpenAI and get the completion, instrumented with LangSmith tracing.
        
        Args:
            prompt (str): The prompt to send to the model
            
        Returns:
            str: The model's response
        """
        try:
            metadata = {
                "session_id": self.session_id,
                "user_id": self.user_id,
                "model": self.model,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }
            
            result = self.lc_llm.invoke(
                prompt,
                config={
                    "callbacks": [self.tracer],
                    "metadata": metadata,
                    "tags": [f"session_{self.session_id}", f"user_{self.user_id}"] if self.user_id else [f"session_{self.session_id}"]
                }
            )
            return result.content
        except Exception as e:
            # Fallback to OpenAI if tracing fails
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
