
# LLM Prompt Application Architecture (Python + OpenAI)

## 🗂 File & Folder Structure

```
llm_app/
├── app/
│   ├── __init__.py
│   ├── main.py                # Entry point of the app
│   ├── config.py              # Environment configuration and API keys
│   ├── prompt_router.py       # Logic for routing/dispatching prompts
│   ├── llm_client.py          # Wrapper for OpenAI API interaction
│   ├── schemas.py             # Data models (e.g., Pydantic)
│   └── utils.py               # Helper functions
│
├── tests/
│   ├── __init__.py
│   ├── test_llm_client.py     # Unit tests for LLM client using mocks
│   ├── test_prompts.py        # Test various prompts and responses
│   └── eval/
│       ├── deepeval_test.py   # Quality tests using DeepEval
│       └── openai_eval.jsonl  # OpenAI Evals formatted testset
│
├── eval/
│   ├── openai_eval_config.yaml  # OpenAI eval configuration
│   └── prompt_variants/         # Variant prompt examples for evaluation
│       ├── task1.jsonl
│       └── task2.jsonl
│
├── requirements.txt
├── README.md
└── .env
```

## 📦 What Each Part Does

### `app/`
- **main.py**: Starts the application, defines routes (if CLI or API), and serves as the orchestrator.
- **config.py**: Loads environment variables (e.g., OpenAI API key) and settings.
- **prompt_router.py**: Defines prompt logic – selects or modifies prompt templates based on use case.
- **llm_client.py**: Handles communication with OpenAI's API (e.g., `openai.ChatCompletion.create`).
- **schemas.py**: Defines request/response formats using Pydantic models.
- **utils.py**: Utility functions (e.g., retry logic, logging setup).

### `tests/`
- **test_llm_client.py**: Mocks OpenAI API calls to ensure the client sends correct payloads and handles errors.
- **test_prompts.py**: Tests correctness and expected outcomes of prompt logic.
- **eval/deepeval_test.py**: Uses DeepEval for regression/quality tests (e.g., faithfulness, coherence).
- **eval/openai_eval.jsonl**: Provides prompt-response pairs for evaluation using OpenAI Evals framework.

### `eval/`
- **openai_eval_config.yaml**: Configuration for running OpenAI evals (e.g., eval type, metrics).
- **prompt_variants/**: Structured test cases for various prompts grouped by task.

### Root Files
- **requirements.txt**: Python dependencies.
- **README.md**: Project overview and setup instructions.
- **.env**: API keys and config variables.

## 🔗 Service Connections

1. **App Startup (`main.py`)**
   - Loads config → Initializes LLM Client → Routes prompt via `prompt_router.py` → Sends to OpenAI via `llm_client.py`.

2. **Prompt Logic (`prompt_router.py`)**
   - Applies templates/variants depending on use case → Returns structured prompt to `llm_client.py`.

3. **LLM Call (`llm_client.py`)**
   - Authenticated OpenAI call with prompt → Receives and returns response.

4. **Testing:**
   - **Unit Tests** (`test_*.py`): Validate prompt structure, API payloads, and error handling.
   - **DeepEval**: Evaluates generated responses using human-aligned metrics.
   - **OpenAI Evals**: Runs large-scale evaluations with predefined scenarios.

## ✅ Example Evaluation Tools

- **DeepEval**:
  - Use `.deepeval_test.py` to evaluate response coherence, correctness, etc.
- **OpenAI Evals**:
  - CLI: `oaiexperiments evaluate openai_eval_config.yaml`
  - Inputs: `openai_eval.jsonl`

## 📌 Notes

- Modular architecture allows reuse of `llm_client` across CLI, web API, or batch apps.
- Easily extendable to support multiple LLMs (e.g., Anthropic, Mistral).
- Testing and eval coverage is decoupled to facilitate high-quality output verification.
