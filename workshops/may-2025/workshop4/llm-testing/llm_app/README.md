# LLM Prompt Application

A Python application for interacting with OpenAI's API to handle prompts, with a focus on modularity, testing, and evaluation.

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
```

## 📊 Evaluation

The project includes evaluation support using OpenAI's evaluation framework:

- Test cases are in `eval/openai_eval.jsonl`
- Configuration is in `eval/openai_eval_config.yaml`

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
