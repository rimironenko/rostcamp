import json
import os
from datetime import datetime

def lambda_handler(event, context):
    """
    AWS Lambda function handler for ChatGPT-like interface.
    
    Expected request format:
    {
        "prompt": "User's input message"
    }
    
    Expected response format:
    {
        "genai_response": "AI generated response"
    }
    """
    
    # Handle CORS preflight requests
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': ''
        }
    
    try:
        # Parse the incoming request
        body = json.loads(event['body'])
        prompt = body.get('prompt', '')
        
        # Validate input
        if not prompt or not prompt.strip():
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS'
                },
                'body': json.dumps({
                    'error': 'Prompt is required'
                })
            }
        
        # Your AI processing logic here
        # This is a simple example - replace with your actual AI service
        response_text = process_prompt(prompt)
        
        # Return the response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'genai_response': response_text
            })
        }
        
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'error': 'Invalid JSON in request body'
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'error': f'Internal server error: {str(e)}'
            })
        }

def process_prompt(prompt):
    """
    Process the user prompt and generate a response.
    Replace this function with your actual AI service integration.
    
    Examples:
    - OpenAI GPT API
    - AWS Bedrock
    - Anthropic Claude
    - Custom AI model
    """
    
    # Simple example response - replace with actual AI processing
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Check for specific keywords to provide different responses
    prompt_lower = prompt.lower()
    
    if 'hello' in prompt_lower or 'hi' in prompt_lower:
        return f"Hello! I'm your AI assistant. The current time is {current_time}. How can I help you today?"
    
    elif 'help' in prompt_lower:
        return """# Help Guide

I'm an AI assistant that can help you with various tasks. Here are some things I can do:

- **Answer questions** about various topics
- **Generate content** like articles, stories, or code
- **Analyze data** and provide insights
- **Help with coding** and debugging

## Example Prompts:
- "Write a Python function to sort a list"
- "Explain machine learning in simple terms"
- "Create a recipe for chocolate chip cookies"

Feel free to ask me anything!"""
    
    elif 'code' in prompt_lower or 'python' in prompt_lower:
        return """Here's a simple Python example:

```python
def greet_user(name):
    \"\"\"
    A simple greeting function
    \"\"\"
    return f"Hello, {name}! Welcome to our application."

# Usage
user_name = "Alice"
message = greet_user(user_name)
print(message)
```

This function takes a name parameter and returns a personalized greeting."""
    
    elif 'weather' in prompt_lower:
        return "I don't have access to real-time weather data, but I can help you with other questions! Try asking me about programming, writing, or general knowledge topics."
    
    else:
        return f"""Thank you for your message: "{prompt}"

I'm a demo AI assistant. In a real implementation, this would be connected to an AI service like:
- OpenAI GPT
- AWS Bedrock
- Anthropic Claude
- Or your custom AI model

Current time: {current_time}

For now, I can provide basic responses. Try asking for help, code examples, or say hello!"""

# Example integration with OpenAI (uncomment and configure as needed)
"""
import openai

def process_prompt_with_openai(prompt):
    # Configure your OpenAI API key
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error processing with OpenAI: {str(e)}"
"""

# Example integration with AWS Bedrock (uncomment and configure as needed)
"""
import boto3

def process_prompt_with_bedrock(prompt):
    bedrock = boto3.client('bedrock-runtime')
    
    try:
        response = bedrock.invoke_model(
            modelId='anthropic.claude-v2',
            body=json.dumps({
                "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                "max_tokens_to_sample": 1000,
                "temperature": 0.7
            })
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['completion']
        
    except Exception as e:
        return f"Error processing with Bedrock: {str(e)}"
""" 