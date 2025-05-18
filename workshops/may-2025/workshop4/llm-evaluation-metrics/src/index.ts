/**
 * src/index.ts
 * Main entry point for the LLM evaluation application
 */

import { evaluateAccuracy } from './evaluators/accuracyEvaluator';
import { evaluateBias } from './evaluators/biasEvaluator';
import { saveResults } from './utils/fileUtils';

// Main function to run both evaluations
async function runEvaluations() {
  try {
    console.log("=== Starting LLM Evaluation ===");
    
    // Run accuracy evaluation
    const accuracyResults = await evaluateAccuracy();
    await saveResults("accuracy_results.json", accuracyResults);
    
    // Run bias evaluation
    const biasResults = await evaluateBias();
    await saveResults("bias_results.json", biasResults);
    
    // Output summary
    console.log("\n=== EVALUATION SUMMARY ===");
    console.log(`Accuracy Score: ${accuracyResults.accuracyScore.toFixed(2)}%`);
    console.log(`Fairness Score (Statistical Parity): ${biasResults.normalizedParityScore.toFixed(2)} (1 is best)`);
    
    // Calculate overall health score (as a simple example)
    const overallHealth = (
      (accuracyResults.accuracyScore / 100) * 0.6 + // Weighting accuracy at 60%
      biasResults.normalizedParityScore * 0.4       // Weighting fairness at 40%
    ) * 100;
    
    console.log(`Overall Model Health Score: ${overallHealth.toFixed(2)}%`);
    
  } catch (error) {
    console.error("Error running evaluations:", error);
  }
}

// Run the application
runEvaluations();