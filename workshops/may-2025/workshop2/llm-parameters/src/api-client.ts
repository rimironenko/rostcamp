/**
 * API client functions for the OpenAI parameter demonstration
 */

import { openai, ParameterConfig, DEFAULT_MODEL, SYSTEM_PROMPT, API_CALL_DELAY_MS, MAX_COMPLETION_TOKENS } from './config';

/**
 * Get a completion from the OpenAI API with the given parameters
 */
export async function getCompletion(
  prompt: string, 
  parameters: Partial<ParameterConfig>
): Promise<string> {
  const start = Date.now();
  
  try {
    // Log API call start
    console.log(`🔄 Calling API with ${parameters.temperature !== undefined ? `temperature=${parameters.temperature}` : ''} ${parameters.top_p !== undefined ? `top_p=${parameters.top_p}` : ''}...`);
    
    const completion = await openai.chat.completions.create({
      model: DEFAULT_MODEL,
      messages: [
        { role: "system", content: SYSTEM_PROMPT },
        { role: "user", content: prompt }
      ],
      temperature: parameters.temperature,
      top_p: parameters.top_p,
      max_completion_tokens: MAX_COMPLETION_TOKENS
    });
    
    const responseTime = Date.now() - start;
    const response = completion.choices[0].message.content?.trim() || '';
    
    // Log response time
    console.log(`✅ API call completed in ${responseTime}ms`);
    
    // Apply the mandatory 1-second delay after each API call
    console.log(`⏱️ Waiting ${API_CALL_DELAY_MS}ms before next API call...`);
    await delay(API_CALL_DELAY_MS);
    
    return response;
  } catch (error) {
    console.error('Error calling OpenAI API:', error);
    
    // Still apply the delay even if there was an error
    console.log(`⏱️ Waiting ${API_CALL_DELAY_MS}ms before next API call...`);
    await delay(API_CALL_DELAY_MS);
    
    throw error;
  }
}

/**
 * Insert a delay between API calls to avoid rate limits
 */
export async function delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}