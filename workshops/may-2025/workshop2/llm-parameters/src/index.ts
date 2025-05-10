/**
 * OpenAI API Parameter Demonstration
 * Main entry point that runs all demonstrations
 */

import { runParameterTests } from './parameter-tests';
import { runMultipleTests } from './multiple-tests';

// Define the prompt to use across all tests
export const COMPLETION_PROMPT = "Please finish the sentence (replace the dots in the end): 'It's raining in the city and all people on the street are ...'. Use just 1 word.";

/**
 * Main function to run the parameter demonstration
 */
async function main() {
  console.log("🔬 OpenAI API Parameter Demonstration 🔬");
  console.log("========================================\n");
  
  console.log(`PROMPT: "${COMPLETION_PROMPT}"`);
  console.log("This prompt demonstrates how parameters affect single-word sentence completion.\n");
  
  // Run the parameter demonstrations
  await runParameterTests();
  
  // Run multiple tests of the same configurations to show variance
  await runMultipleTests();
}

// Run the demonstration
main().catch(error => {
  console.error("Error in parameter demonstration:", error);
});