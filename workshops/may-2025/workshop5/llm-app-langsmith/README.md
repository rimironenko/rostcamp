# LLM Application with LangSmith Integration

This project is a simple LLM application that uses OpenAI's API to generate responses to user prompts. It also integrates with LangSmith for tracing and monitoring LLM calls, and includes a local dashboard for evaluation metrics and feedback.

## Features

- **OpenAI Integration**: Uses OpenAI's API to generate responses.
- **LangSmith Integration**: Traces and monitors LLM calls using LangSmith.
- **Local Dashboard**: A local dashboard is available for viewing evaluation metrics and user feedback.

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory with the following variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   LANGSMITH_API_KEY=your_langsmith_api_key
   LANGSMITH_PROJECT=your_langsmith_project_name
   ```

5. **Run the application**:
   ```bash
   python -m app.main
   ```

6. **Access the local dashboard**:
   The local dashboard is available at `http://localhost:8000` (or the port specified in your configuration).

## Testing

Run the automated tests using pytest:
```bash
python -m pytest tests/ -v
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🚀 Setup

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory with:
   ```
   OPENAI_API_KEY=your-api-key-here
   MODEL_NAME=gpt-3.5-turbo
   ```

## 💻 Usage

Run the CLI application:
```bash
python -m app.main
```

The application will:
1. Prompt you for input
2. Route your prompt through the router
3. Send it to OpenAI
4. Display the response

## 🧪 Testing

Run all tests:
```bash
python -m pytest
```

Run specific test files:
```bash
python -m pytest tests/test_llm_client.py
python -m pytest tests/test_prompts.py
python -m pytest tests/test_openai_eval.py   # OpenAI Eval tests
python -m pytest tests/test_deepeval.py      # DeepEval tests
```

## 📊 Evaluation

The project includes evaluation support using both OpenAI's evaluation framework and DeepEval:

### OpenAI Eval
- Test cases are in `eval/openai_eval.jsonl` (edit or add your own for custom evaluation)
- Configuration is in `eval/openai_eval_config.yaml`
- To run the OpenAI Eval tests:
  ```bash
  python -m pytest tests/test_openai_eval.py -v
  ```
- These tests check LLM responses for accuracy, relevance, coherence, and helpfulness, using the prompts and expected answers in the dataset.

### DeepEval
- DeepEval tests are in `tests/test_deepeval.py`
- These tests use DeepEval's metrics (hallucination, answer relevancy, etc.) to evaluate LLM responses
- To run DeepEval tests:
  ```bash
  python -m pytest tests/test_deepeval.py -v
  ```
- You can add or modify test cases in the file to suit your evaluation needs.

## 📁 Project Structure

```
llm_app/
├── app/
│   ├── main.py          # CLI entry point
│   ├── config.py        # Environment configuration
│   ├── llm_client.py    # OpenAI API interaction
│   ├── prompt_router.py # Prompt routing logic
│   ├── schemas.py       # Data models
│   └── utils.py         # Helper functions
├── tests/               # Unit tests
├── eval/                # Evaluation files
├── requirements.txt     # Dependencies
└── .env                 # Environment variables
```

## 🔧 Development

- All code changes should be tested
- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed

## Running the Local Dashboard

To run the local dashboard, follow these steps:

1. Ensure your application is running:
   ```bash
   python -m app.main
   ```

2. In a separate terminal, run the dashboard server:
   ```bash
   python -m app.dashboard
   ```

3. Open your web browser and navigate to:
   ```
   http://localhost:8000
   ```
   (or the port specified in your configuration)

The dashboard provides real-time metrics and feedback for your LLM application.
