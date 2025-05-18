import { EvalExample } from "../types/evaluationTypes";

/**
 * Returns the dataset for accuracy evaluation
 */
export function getAccuracyExamples(): EvalExample[] {
  return [
    {
      input: "What is the capital of France?",
      ideal: "Paris"
    },
    {
      input: "Who wrote 'Pride and Prejudice'?",
      ideal: "Jane Austen"
    },
    {
      input: "What is the chemical symbol for gold?",
      ideal: "Au"
    },
    {
      input: "What year did World War II end?",
      ideal: "1945"
    },
    {
      input: "What is the largest planet in our solar system?",
      ideal: "Jupiter"
    },
    {
      input: "What is the boiling point of water in Celsius?",
      ideal: "100"
    },
    {
      input: "Who painted the Mona Lisa?",
      ideal: "Leonardo da Vinci"
    },
    {
      input: "What is the capital of Japan?",
      ideal: "Tokyo"
    },
    {
      input: "What is the square root of 64?",
      ideal: "8"
    },
    {
      input: "Who was the first president of the United States?",
      ideal: "George Washington"
    }
  ];
}