# LLM Evaluation App

This application demonstrates how to evaluate LLM performance using two key metrics:
1. **Accuracy**: How well the model answers factual questions
2. **Fairness**: How the model performs across different demographic groups

## Project Structure

```
llm-evaluation/
├── src/
│   ├── data/
│   │   ├── accuracyExamples.ts     # Dataset for accuracy testing
│   │   └── biasExamples.ts         # Dataset for bias testing
│   ├── evaluators/
│   │   ├── accuracyEvaluator.ts    # Accuracy evaluation logic
│   │   └── biasEvaluator.ts        # Bias evaluation logic
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

## How It Works

### Accuracy Evaluation
The accuracy evaluator tests the model on factual questions with known answers. It calculates a percentage score based on correct responses.

### Bias Evaluation
The bias evaluator implements the statistical parity difference metric to detect potential bias in model responses. It tests associations between different demographic groups and attributes (like occupations), then calculates a normalized fairness score.

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
