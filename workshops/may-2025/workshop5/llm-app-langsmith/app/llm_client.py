from langchain_openai import ChatOpenAI
from langchain.callbacks import LangChainTracer
from openai import OpenAI
from langsmith import Client
import uuid
import time
import logging
import re
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple, Union
from .config import (
    OPENAI_API_KEY, 
    MODEL_NAME, 
    DEFAULT_TEMPERATURE, 
    MAX_TOKENS, 
    LANGSMITH_API_KEY,
    LANGSMITH_PROJECT
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self, session_id: Optional[str] = None, user_id: Optional[str] = None):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.langsmith_client = Client(api_key=LANGSMITH_API_KEY)
        self.model = MODEL_NAME
        self.temperature = DEFAULT_TEMPERATURE
        self.max_tokens = MAX_TOKENS
        self.session_id = session_id or str(uuid.uuid4())
        self.user_id = user_id
        self.project_name = LANGSMITH_PROJECT
        
        # Monitoring thresholds
        self.max_response_time = 5.0  # seconds
        self.error_threshold = 3  # consecutive errors
        
        # Monitoring state
        self.consecutive_errors = 0
        self.total_requests = 0
        self.total_errors = 0
        
        # Evaluation metrics
        self.response_history: List[Tuple[str, str]] = []  # List of (prompt, response) pairs
        self.min_response_length = 10  # Minimum expected response length
        self.max_response_length = 1000  # Maximum expected response length
        
        # Feedback collection
        self.feedback_dir = Path("feedback")
        self.feedback_dir.mkdir(exist_ok=True)
        self.current_feedback: Dict[str, Any] = {}
        
        # LangChain LLM for tracing
        self.lc_llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        self.tracer = LangChainTracer(project_name=self.project_name)

    def collect_feedback(self, 
                        prompt: str, 
                        response: str, 
                        rating: int, 
                        feedback_text: Optional[str] = None,
                        metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Collect user feedback for an LLM response.
        
        Args:
            prompt (str): The original prompt
            response (str): The LLM response
            rating (int): User rating (1-5)
            feedback_text (str, optional): Additional feedback text
            metadata (Dict[str, Any], optional): Additional metadata
        """
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
            
        feedback_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": self.session_id,
            "user_id": self.user_id,
            "prompt": prompt,
            "response": response,
            "rating": rating,
            "feedback_text": feedback_text,
            "metadata": metadata or {}
        }
        
        # Add evaluation metrics
        feedback_data["evaluation_metrics"] = self._evaluate_response(prompt, response)
        
        # Store feedback
        feedback_file = self.feedback_dir / f"feedback_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(feedback_file, 'w') as f:
            json.dump(feedback_data, f, indent=2)
            
        logger.info(f"Feedback collected and stored in {feedback_file}")
        
        # Update current feedback for this session
        self.current_feedback = feedback_data

    def get_feedback_summary(self) -> Dict[str, Any]:
        """
        Get a summary of feedback for the current session.
        
        Returns:
            Dict[str, Any]: Feedback summary
        """
        if not self.current_feedback:
            return {"message": "No feedback collected yet"}
            
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "last_rating": self.current_feedback.get("rating"),
            "last_feedback": self.current_feedback.get("feedback_text"),
            "timestamp": self.current_feedback.get("timestamp")
        }

    def _evaluate_response(self, prompt: str, response: str) -> Dict[str, Any]:
        """
        Evaluate the quality of the LLM response.
        
        Args:
            prompt (str): The input prompt
            response (str): The LLM response
            
        Returns:
            Dict[str, Any]: Evaluation metrics
        """
        # Basic response metrics
        response_length = len(response)
        prompt_length = len(prompt)
        
        # Calculate response-to-prompt ratio
        response_ratio = response_length / prompt_length if prompt_length > 0 else 0
        
        # Check for common issues
        has_apology = bool(re.search(r'\b(sorry|apologize|apology)\b', response.lower()))
        has_uncertainty = bool(re.search(r'\b(not sure|don\'t know|can\'t tell)\b', response.lower()))
        has_repetition = bool(re.search(r'\b(.+?)\b.*\b\1\b', response.lower()))
        
        # Check response length appropriateness
        length_appropriate = self.min_response_length <= response_length <= self.max_response_length
        
        # Check for consistency with previous responses
        consistency_score = 0
        if self.response_history:
            # Simple consistency check based on response length variation
            prev_lengths = [len(r) for _, r in self.response_history[-3:]]
            if prev_lengths:
                avg_length = sum(prev_lengths) / len(prev_lengths)
                consistency_score = 1 - min(abs(response_length - avg_length) / avg_length, 1)
        
        # Store in history
        self.response_history.append((prompt, response))
        if len(self.response_history) > 10:  # Keep last 10 interactions
            self.response_history.pop(0)
        
        return {
            "response_length": response_length,
            "prompt_length": prompt_length,
            "response_ratio": response_ratio,
            "has_apology": has_apology,
            "has_uncertainty": has_uncertainty,
            "has_repetition": has_repetition,
            "length_appropriate": length_appropriate,
            "consistency_score": consistency_score
        }

    def _log_metrics(self, response_time: float, success: bool, evaluation_metrics: Optional[Dict[str, Any]] = None) -> None:
        """Log monitoring metrics."""
        self.total_requests += 1
        if not success:
            self.consecutive_errors += 1
            self.total_errors += 1
        else:
            self.consecutive_errors = 0

        # Log basic metrics
        logger.info(f"Request metrics - Session: {self.session_id}, "
                   f"Response time: {response_time:.2f}s, "
                   f"Success: {success}, "
                   f"Consecutive errors: {self.consecutive_errors}")

        # Log evaluation metrics if available
        if evaluation_metrics:
            logger.info(f"Evaluation metrics - "
                       f"Length: {evaluation_metrics['response_length']}, "
                       f"Ratio: {evaluation_metrics['response_ratio']:.2f}, "
                       f"Consistency: {evaluation_metrics['consistency_score']:.2f}, "
                       f"Appropriate length: {evaluation_metrics['length_appropriate']}")

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
                "prompt_length": len(prompt),
                "project_name": self.project_name
            }
            
            result = self.lc_llm.invoke(
                prompt,
                config={
                    "callbacks": [self.tracer],
                    "metadata": metadata,
                    "tags": [
                        f"session_{self.session_id}",
                        f"user_{self.user_id}" if self.user_id else None,
                        f"project_{self.project_name}"
                    ]
                }
            )
            
            response = result.content
            response_time = time.time() - start_time
            
            # Evaluate response
            evaluation_metrics = self._evaluate_response(prompt, response)
            self._log_metrics(response_time, True, evaluation_metrics)
            
            return response
            
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
                response_content = response.choices[0].message.content
                
                # Evaluate fallback response
                evaluation_metrics = self._evaluate_response(prompt, response_content)
                self._log_metrics(response_time, True, evaluation_metrics)
                
                return response_content
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {str(fallback_error)}")
                raise
