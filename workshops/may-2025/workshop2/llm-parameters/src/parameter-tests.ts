/**
 * Run single tests with different parameter configurations
 */

import { parameterConfigs } from './config';
import { getCompletion } from './api-client';
import { COMPLETION_PROMPT } from './index';

/**
 * Run tests with different parameter configurations
 */
export async function runParameterTests(): Promise<void> {
  for (const config of parameterConfigs) {
    try {
      console.log(`\n🔹 ${config.name} 🔹`);
      console.log(config.description);
      
      const response = await getCompletion(COMPLETION_PROMPT, config);
      
      console.log("\nResponse:");
      console.log(`"${response}"`);
      console.log("\n----------------------------------------\n");
      
      // No need for additional delay here as getCompletion already includes the delay
    } catch (error) {
      console.error(`Error with ${config.name}:`, error);
    }
  }
}