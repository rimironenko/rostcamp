#!/usr/bin/env ts-node
// A utility to test prompts against guardrails

import { templates } from '../config/prompt-templates';
import openAIService from '../services/openai-service';

async function main() {
  // Get command line arguments
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.log('Usage: npm run validate [template-name] [input-text]');
    console.log('\nAvailable templates:');
    Object.keys(templates).forEach(name => console.log(`- ${name}`));
    process.exit(1);
  }

  const templateName = args[0];
  const userInput = args[1];

  // Find the template
  const templateKey = templateName as keyof typeof templates;
  const template = templates[templateKey];

  if (!template) {
    console.error(`Template "${templateName}" not found. Available templates:`);
    Object.keys(templates).forEach(name => console.log(`- ${name}`));
    process.exit(1);
  }

  console.log(`Testing template: ${template.name}`);
  console.log(`Input: "${userInput}"`);
  console.log('\nSending request to OpenAI...');

  try {
    // Run the prompt with guardrails
    const result = await openAIService.promptWithGuardrails(template, userInput);

    console.log('\n--- RESULTS ---');
    console.log(`Valid: ${result.isValid ? 'Yes ✅' : 'No ❌'}`);
    
    if (result.errors.length > 0) {
      console.log('\nErrors:');
      result.errors.forEach(error => {
        console.log(`- [${error.guardrail}] ${error.message}`);
      });
    }
    
    if (result.warnings.length > 0) {
      console.log('\nWarnings:');
      result.warnings.forEach(warning => {
        console.log(`- [${warning.guardrail}] ${warning.message}`);
      });
    }

    console.log('\nRaw Response:');
    console.log('-------------');
    console.log(result.rawResponse);
    console.log('-------------');

    if (result.processedResponse) {
      console.log('\nProcessed Response:');
      console.log(JSON.stringify(result.processedResponse, null, 2));
    }
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

// Run the main function
main().catch(console.error);