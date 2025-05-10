/**
 * Integration tests for the OpenAI service with templates
 * 
 * Note: These tests require a valid OpenAI API key and will make actual API calls.
 * To run these tests, you need to have a valid API key in your .env file.
 * 
 * You can run only the unit tests with: npm test -- --testPathIgnorePatterns=integration
 */

import openAIService from '../services/openai-service';
import { templates } from '../config/prompt-templates';

// Skip these tests if no API key or in CI environment
const runIntegrationTests = process.env.OPENAI_API_KEY && !process.env.CI;

// Use conditional test execution
const testFn = runIntegrationTests ? describe : describe.skip;

testFn('Integration tests', () => {
  // Add longer timeout for API calls
  jest.setTimeout(30000);
  
  it('should generate a product description with guardrails', async () => {
    const result = await openAIService.promptWithGuardrails(
      templates.productDescription,
      'Wireless earbuds with noise cancellation'
    );
    
    expect(result.isValid).toBe(true);
    expect(result.processedResponse).toHaveProperty('title');
    expect(result.processedResponse).toHaveProperty('description');
    expect(result.processedResponse).toHaveProperty('keyFeatures');
    expect(Array.isArray(result.processedResponse.keyFeatures)).toBe(true);
  });
  
  it('should moderate content correctly', async () => {
    const result = await openAIService.promptWithGuardrails(
      templates.contentModeration,
      'This is a normal message about technology.'
    );
    
    expect(result.isValid).toBe(true);
    expect(result.rawResponse).toContain('appropriate');
  });
});