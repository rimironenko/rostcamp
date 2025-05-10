import { ChatCompletionCreateParams, ChatCompletionMessageParam } from 'openai/resources/chat';
import { openai, MODELS, DEFAULT_PARAMS } from '../config/openai';
import type { PromptTemplate, ValidationResult } from '../config/prompt-types';
import { validateResponse } from '../guardrails/validator';

export class OpenAIService {
  /**
   * Sends a prompt to the OpenAI API with guardrails
   */
  async promptWithGuardrails(
    template: PromptTemplate, 
    userInput: string,
    additionalParams: Partial<ChatCompletionCreateParams> = {}
  ): Promise<ValidationResult> {
    // Generate the user prompt from the template
    const userPrompt = template.userPromptTemplate.replace(/\{input\}/g, userInput);
    
    // Create the API request using helper function
   const messages: ChatCompletionMessageParam[] = [
      { role: 'system', content: template.systemPrompt },
      { role: 'user', content: userPrompt }
    ];

    try {
      // Send the request to OpenAI
      const completion = await openai.chat.completions.create({
        model: MODELS.DEFAULT,
        messages,
        ...DEFAULT_PARAMS,
        ...additionalParams
      });

      // Use helper function to extract content safely
      if (!('choices' in completion) || !completion.choices || completion.choices.length === 0) {
        throw new Error('Unexpected response format from OpenAI API');
      }

      const response = completion.choices[0].message.content || '';
      
      // Validate the response against guardrails
      return await validateResponse(response, template);
    } catch (error) {
      console.error('Error calling OpenAI API:', error);
      throw error;
    }
  }

  /**
   * Retry with fallback model if primary model fails
   */
  async promptWithFallback(
    template: PromptTemplate, 
    userInput: string,
    additionalParams: Partial<ChatCompletionCreateParams> = {}
  ): Promise<ValidationResult> {
    try {
      return await this.promptWithGuardrails(template, userInput, additionalParams);
    } catch (error) {
      console.warn('Primary model failed, trying fallback model');
      // Try with fallback model
      return await this.promptWithGuardrails(
        template, 
        userInput, 
        { ...additionalParams, model: MODELS.FALLBACK }
      );
    }
  }
}

export default new OpenAIService();