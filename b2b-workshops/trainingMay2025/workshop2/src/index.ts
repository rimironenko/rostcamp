import { templates } from './config/prompt-templates';
import openAIService from './services/openai-service';

async function main() {
  try {
    // Demo using a template with guardrails
    console.log("Testing product description template...");
    
    const productInput = "Wireless noise-cancelling headphones with 30-hour battery life, water resistance, and multi-device connectivity";
    const result = await openAIService.promptWithGuardrails(
      templates.productDescription, 
      productInput
    );

    if (result.isValid) {
      console.log("Response passed all guardrails!");
      console.log("\nFormatted Response:");
      console.log(JSON.stringify(result.processedResponse, null, 2));
    } else {
      console.log("Response failed guardrails:");
      
      result.errors.forEach(error => {
        console.log(`- ERROR [${error.guardrail}]: ${error.message}`);
      });
      
      result.warnings.forEach(warning => {
        console.log(`- WARNING [${warning.guardrail}]: ${warning.message}`);
      });
      
      console.log("\nRaw Response:");
      console.log(result.rawResponse);
    }

    // Example of content moderation
    console.log("\n\nTesting content moderation template...");
    const moderationInput = "I really enjoyed the movie last night!";
    const moderationResult = await openAIService.promptWithGuardrails(
      templates.contentModeration, 
      moderationInput
    );

    console.log("\nModeration result:");
    console.log(moderationResult.rawResponse);
    
  } catch (error) {
    console.error("Error:", error);
  }
}

// Run the main function
main();