# 📋 Step-by-Step MVP Build Plan for LLM Prompt App

This document provides an extremely granular, testable task plan to build an MVP based on the given architecture.

---

## Phase 1: Project Setup

### 1.1 - Create Project Directory
- **Start:** No folder exists
- **End:** `llm_app/` directory created

### 1.2 - Initialize Git Repository
- **Start:** Inside `llm_app/`
- **End:** Git initialized with `.gitignore`

### 1.3 - Set Up Virtual Environment
- **Start:** Python installed
- **End:** `venv` activated, `.venv/` created

### 1.4 - Create Initial File Structure
- **Start:** Inside project folder
- **End:** All files and folders from architecture scaffold created

---

## Phase 2: Core Application Logic

### 2.1 - Implement `config.py`
- **Start:** Empty file
- **End:** Reads `.env` for API keys and sets config variables

### 2.2 - Implement `llm_client.py` (Basic)
- **Start:** Empty file
- **End:** Sends simple prompt to OpenAI and receives output

### 2.3 - Implement `schemas.py`
- **Start:** Empty file
- **End:** Defines Pydantic model for input/output prompt data

### 2.4 - Implement `prompt_router.py` (Stub)
- **Start:** Empty file
- **End:** Returns static template string based on stub logic

### 2.5 - Implement `main.py` (CLI mode)
- **Start:** Empty file
- **End:** Accepts user prompt from CLI, routes through router → OpenAI → prints result

---

## Phase 3: Utility & Testing Foundation

### 3.1 - Implement `utils.py` (Logger)
- **Start:** Empty file
- **End:** Adds a logger that prints to console

### 3.2 - Write `test_llm_client.py`
- **Start:** Empty test file
- **End:** Mocks API response and validates payload

### 3.3 - Write `test_prompts.py`
- **Start:** Empty test file
- **End:** Tests static routing logic in `prompt_router.py`

---

## Phase 4: Evaluation Support

### 4.1 - Add `openai_eval.jsonl` File
- **Start:** No eval set
- **End:** Contains 2-3 prompt-response pairs for testing

### 4.2 - Add `openai_eval_config.yaml`
- **Start:** Empty file
- **End:** Defines metrics, model, and dataset path

---

## Phase 5: Finalization

### 5.1 - Add `.env` File
- **Start:** Non-existent
- **End:** Contains `OPENAI_API_KEY` and env variables

### 5.2 - Fill Out `README.md`
- **Start:** Empty README
- **End:** Explains setup, usage, and evaluation

### 5.3 - Populate `requirements.txt`
- **Start:** Empty
- **End:** Includes FastAPI, Pydantic, OpenAI, pytest, python-dotenv

---

## ✅ Done!
This MVP now supports CLI prompt interaction with OpenAI, test coverage, and evaluation readiness.