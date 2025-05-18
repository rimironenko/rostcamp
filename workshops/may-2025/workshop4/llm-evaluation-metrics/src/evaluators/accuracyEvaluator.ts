/**
 * src/evaluators/accuracyEvaluator.ts
 * Implements accuracy evaluation using OpenAI Evals principles
 */

import { openai } from '../utils/openaiClient';
import { EvalExample } from '../types/evaluationTypes';
import { getAccuracyExamples } from '../data/accuracyExamples';

/**
 * Evaluates the accuracy of the model on factual questions
 */
export async function evaluateAccuracy() {
  console.log("Starting accuracy evaluation...");
  
  // Get examples from our dataset
  const accuracyExamples: EvalExample[] = getAccuracyExamples();

  const results = [];
  let correctCount = 0;

  for (const example of accuracyExamples) {
    console.log(`Testing: ${example.input}`);
    
    try {
      const response = await openai.chat.completions.create({
        model: "gpt-3.5-turbo",
        messages: [
          { role: "system", content: "You are a helpful assistant that provides concise, factual responses." },
          { role: "user", content: example.input }
        ],
        temperature: 0.2,
        max_tokens: 50
      });

      const output = response.choices[0].message.content?.trim() || "";
      
      // Simple exact match or contains evaluation
      // In a real app, you'd use more sophisticated matching
      const isCorrect = output.toLowerCase().includes(example.ideal.toLowerCase());
      
      if (isCorrect) correctCount++;
      
      results.push({
        input: example.input,
        ideal: example.ideal,
        output: output,
        isCorrect: isCorrect
      });
      
    } catch (error) {
      console.error(`Error evaluating example: ${example.input}`, error);
      results.push({
        input: example.input,
        ideal: example.ideal,
        output: "ERROR",
        isCorrect: false
      });
    }
  }

  const accuracyScore = (correctCount / accuracyExamples.length) * 100;
  
  console.log(`Accuracy Evaluation Complete: ${accuracyScore.toFixed(2)}%`);
  
  return {
    accuracyScore,
    detailedResults: results
  }
};