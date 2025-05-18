/**
 * src/index.ts
 * Main entry point for the LLM evaluation application
 */

import { evaluateAccuracy } from './evaluators/accuracyEvaluator';
import { evaluateBias } from './evaluators/biasEvaluator';
import { evaluateAdvancedBias } from './evaluators/advancedBiasEvaluator';
import { saveResults } from './utils/fileUtils';


// Main function to run evaluations
async function runEvaluations() {
  try {
    console.log("=== Starting LLM Evaluation ===");
    
    // Run accuracy evaluation
    console.log("\n=== Running Accuracy Evaluation ===");
    const accuracyResults = await evaluateAccuracy();
    await saveResults("accuracy_results.json", accuracyResults);
    
    // Run basic bias evaluation
    console.log("\n=== Running Basic Bias Evaluation ===");
    const basicBiasResults = await evaluateBias();
    await saveResults("basic_bias_results.json", basicBiasResults);
    
    // Run advanced bias evaluation
    console.log("\n=== Running Advanced Bias Evaluation ===");
    const advancedBiasResults = await evaluateAdvancedBias();
    await saveResults("advanced_bias_results.json", advancedBiasResults);
    
    // Output summary
    console.log("\n=== EVALUATION SUMMARY ===");
    console.log(`Accuracy Score: ${accuracyResults.accuracyScore.toFixed(2)}%`);
    console.log(`Basic Fairness Score (Statistical Parity): ${basicBiasResults.normalizedParityScore.toFixed(4)} (1 is best)`);
    console.log(`Advanced Fairness Score (Embedding Association): ${advancedBiasResults.normalizedBiasScore.toFixed(4)} (1 is best)`);
    
    // Calculate overall health score (as a simple example)
    const overallHealth = (
      (accuracyResults.accuracyScore / 100) * 0.5 +          // Weighting accuracy at 50%
      basicBiasResults.normalizedParityScore * 0.2 +         // Weighting basic fairness at 20%
      advancedBiasResults.normalizedBiasScore * 0.3          // Weighting advanced fairness at 30%
    ) * 100;
    
    console.log(`Overall Model Health Score: ${overallHealth.toFixed(2)}%`);
    
    // Provide bias insights
    console.log("\n=== BIAS INSIGHTS ===");
    for (const result of advancedBiasResults.detailedResults.slice(0, 5)) {
      console.log(`- ${result.attribute}: ${result.interpretation}`);
    }
    
  } catch (error) {
    console.error("Error running evaluations:", error);
  }
}

// Run the application
runEvaluations();
