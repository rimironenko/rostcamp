from langchain_openai import ChatOpenAI
from langchain.callbacks import LangChainTracer
from openai import OpenAI
from langsmith import Client
import uuid
import time
import logging
from typing import Optional, Dict, Any
from .config import OPENAI_API_KEY, MODEL_NAME, DEFAULT_TEMPERATURE, MAX_TOKENS, LANGSMITH_API_KEY

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        
        # Monitoring thresholds
        self.max_response_time = 5.0  # seconds
        self.error_threshold = 3  # consecutive errors
        
        # Monitoring state
        self.consecutive_errors = 0
        self.total_requests = 0
        self.total_errors = 0
        
        # LangChain LLM for tracing
        self.lc_llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        self.tracer = LangChainTracer()

    def _log_metrics(self, response_time: float, success: bool) -> None:
        """Log monitoring metrics."""
        self.total_requests += 1
        if not success:
            self.consecutive_errors += 1
            self.total_errors += 1
        else:
            self.consecutive_errors = 0

        # Log metrics
        logger.info(f"Request metrics - Session: {self.session_id}, "
                   f"Response time: {response_time:.2f}s, "
                   f"Success: {success}, "
                   f"Consecutive errors: {self.consecutive_errors}")

        # Alert on thresholds
        if response_time > self.max_response_time:
            logger.warning(f"High response time alert: {response_time:.2f}s > {self.max_response_time}s")
        
        if self.consecutive_errors >= self.error_threshold:
            logger.error(f"Error threshold exceeded: {self.consecutive_errors} consecutive errors")

    def get_completion(self, prompt: str) -> str:
        """
        Send a prompt to OpenAI and get the completion, instrumented with LangSmith tracing.
        
        Args:
            prompt (str): The prompt to send to the model
            
        Returns:
            str: The model's response
        """
        start_time = time.time()
        try:
            metadata = {
                "session_id": self.session_id,
                "user_id": self.user_id,
                "model": self.model,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "prompt_length": len(prompt)
            }
            
            result = self.lc_llm.invoke(
                prompt,
                config={
                    "callbacks": [self.tracer],
                    "metadata": metadata,
                    "tags": [f"session_{self.session_id}", f"user_{self.user_id}"] if self.user_id else [f"session_{self.session_id}"]
                }
            )
            
            response_time = time.time() - start_time
            self._log_metrics(response_time, True)
            return result.content
            
        except Exception as e:
            response_time = time.time() - start_time
            self._log_metrics(response_time, False)
            logger.error(f"Error in get_completion: {str(e)}")
            
            # Fallback to OpenAI if tracing fails
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                return response.choices[0].message.content
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {str(fallback_error)}")
                raise
