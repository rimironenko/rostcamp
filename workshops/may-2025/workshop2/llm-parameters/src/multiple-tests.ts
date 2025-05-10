/**
 * Run multiple tests with the same parameters to show variance
 */

import { multiRunConfigs, NUM_MULTIPLE_RUNS } from './config';
import { getCompletion, delay } from './api-client';
import { COMPLETION_PROMPT } from './index';

/**
 * Analyze the uniqueness of responses
 */
function analyzeUniqueness(responses: string[]): {
  uniqueCount: number;
  uniquenessPercentage: number;
  uniqueResponses: string[];
} {
  const uniqueResponses = [...new Set(responses)];
  const uniqueCount = uniqueResponses.length;
  const uniquenessPercentage = (uniqueCount / responses.length) * 100;
  
  return {
    uniqueCount,
    uniquenessPercentage,
    uniqueResponses
  };
}

/**
 * Run multiple tests with the same parameters
 */
export async function runMultipleTests(): Promise<void> {
  console.log("\nMULTIPLE RUNS WITH SAME PARAMETERS");
  console.log(`Running the same prompt ${NUM_MULTIPLE_RUNS} times with each parameter set to show consistency/variation.\n`);
  
  for (const config of multiRunConfigs) {
    console.log(`\n🔹 ${config.name} 🔹`);
    console.log(`Running the same prompt ${NUM_MULTIPLE_RUNS} times with ${config.name} to demonstrate consistency/variation:\n`);
    
    const responses: string[] = [];
    
    for (let i = 1; i <= NUM_MULTIPLE_RUNS; i++) {
      try {
        const response = await getCompletion(COMPLETION_PROMPT, config);
        responses.push(response);
        console.log(`Run ${i}: ${response}`);
        
        // Small delay between requests
        await delay(500);
      } catch (error) {
        console.error(`Error in run ${i}:`, error);
      }
    }
    
    // Analyze and display statistics
    const { uniqueCount, uniquenessPercentage, uniqueResponses } = analyzeUniqueness(responses);
    
    console.log(`\nStats: ${uniqueCount} unique responses out of ${responses.length} runs (${uniquenessPercentage.toFixed(1)}% uniqueness)`);
    console.log(`Unique responses: ${uniqueResponses.join(', ')}`);
    console.log("\n----------------------------------------");
  }
}