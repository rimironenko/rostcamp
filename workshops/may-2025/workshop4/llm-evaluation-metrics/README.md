# LLM Evaluation App

This application demonstrates how to evaluate LLM performance using two key metrics:
1. **Accuracy**: How well the model answers factual questions
2. **Fairness**: How the model performs across different demographic groups, using both basic and advanced bias detection methods

## Key Features

- **Simple but effective accuracy testing**: Uses a straightforward approach to evaluate factual correctness
- **Two-tier bias evaluation**:
  - Basic statistical parity measurement: Quantifies bias using association differences
  - Advanced embedding-based analysis: Uses OpenAI embeddings to detect subtle biases through word associations
- **Detailed result logging**: Saves all evaluation results to JSON files for further analysis
- **Summary metrics**: Provides an overall model health score weighted between accuracy and multiple fairness metrics

## Project Structure

```
llm-evaluation/
├── src/
│   ├── data/
│   │   ├── accuracyExamples.ts     # Dataset for accuracy testing
│   │   └── biasExamples.ts         # Dataset for bias testing
│   ├── evaluators/
│   │   ├── accuracyEvaluator.ts    # Accuracy evaluation logic
│   │   ├── biasEvaluator.ts        # Basic bias evaluation logic
│   │   └── advancedBiasEvaluator.ts # Advanced embedding-based bias evaluation
│   ├── types/
│   │   └── evaluationTypes.ts      # Type definitions
│   ├── utils/
│   │   ├── fileUtils.ts            # File handling utilities
│   │   └── openaiClient.ts         # OpenAI client configuration
│   └── index.ts                    # Main application entry point
├── results/                        # Evaluation results (created on run)
├── package.json
├── tsconfig.json
└── .env                           # Environment variables (create this)
```

## Setup Instructions

1. Clone this repository
   ```bash
   git clone https://github.com/rimironenko/rostcamp.git
   cd workshops/may-2025/workshop4/llm-evaluation-metrics
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
4. Build and run the evaluation:
   ```bash
   npm run build
   npm start
   ```
   
   Alternatively, you can run in development mode without a separate build step:
   ```bash
   npm run dev
   ```

## How It Works

### Accuracy Evaluation
The accuracy evaluator tests the model on factual questions with known answers. It calculates a percentage score based on correct responses.

### Bias Evaluation
The application provides two bias evaluation approaches:

1. **Basic Bias Evaluator** - Tests the model's associations between different demographic groups and attributes (like occupations) using direct querying, then calculates a statistical parity score.

2. **Advanced Bias Evaluator** - Uses OpenAI's text embeddings to implement a technique similar to Word Embedding Association Test (WEAT), a scientifically validated method for detecting bias in language models. It computes:
   - Cosine similarity between attribute and demographic group embeddings
   - Effect sizes (similar to Cohen's d) to quantify bias
   - Detailed interpretations of detected biases

## Customization

You can customize the evaluations by:
- Adding more examples to the datasets in `src/data/`
- Modifying the evaluation logic in `src/evaluators/`
- Changing the model parameters in the evaluator files
- Adjusting how the overall health score is calculated in `index.ts`

## Requirements

- Node.js 14+
- OpenAI API key

## Extending the Framework

This demonstration can be extended by:
- Adding more evaluation metrics
- Integrating with formal OpenAI Evals
- Implementing more sophisticated matching algorithms
- Creating a web interface for results visualization
