import type { PromptTemplate, ValidationResult, ValidationError, ValidationWarning } from '../config/prompt-types';
import { ZodError } from 'zod';

/**
 * Validates a response against the guardrails defined in the prompt template
 */
export async function validateResponse(
  response: string,
  template: PromptTemplate
): Promise<ValidationResult> {
  const errors: ValidationError[] = [];
  const warnings: ValidationWarning[] = [];
  
  // Skip validation if no guardrails are defined
  if (!template.guardrails || template.guardrails.length === 0) {
    return {
      isValid: true,
      errors,
      warnings,
      rawResponse: response
    };
  }

  // Apply each guardrail check
  for (const guardrail of template.guardrails) {
    try {
      const passed = await guardrail.check(response);
      
      if (!passed) {
        const issue = {
          guardrail: guardrail.name,
          message: guardrail.description
        };
        
        if (guardrail.severity === 'error') {
          errors.push(issue);
        } else {
          warnings.push(issue);
        }
      }
    } catch (error) {
      console.error(`Error in guardrail "${guardrail.name}":`, error);
      errors.push({
        guardrail: guardrail.name,
        message: `Guardrail check failed: ${error instanceof Error ? error.message : String(error)}`
      });
    }
  }

  // Validate against schema if provided
  let processedResponse: any = undefined;
  
  if (template.expectedResponseSchema) {
    try {
      processedResponse = template.expectedResponseSchema.parse(
        // Attempt to parse JSON if the response looks like JSON
        response.trim().startsWith('{') ? JSON.parse(response) : response
      );
    } catch (error) {
      if (error instanceof ZodError) {
        errors.push({
          guardrail: 'schema_validation',
          message: `Response does not match expected schema: ${error.message}`
        });
      } else {
        errors.push({
          guardrail: 'json_parsing',
          message: `Failed to parse response as JSON: ${error instanceof Error ? error.message : String(error)}`
        });
      }
    }
  }

  return {
    isValid: errors.length === 0,
    errors,
    warnings,
    rawResponse: response,
    processedResponse
  };
}

/**
 * Filter sensitive information from the response
 */
export function sanitizeResponse(response: string): string {
  // Example implementation - replace with your specific requirements
  return response
    .replace(/\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b/g, '[REDACTED SSN]')
    .replace(/\b\d{16}\b/g, '[REDACTED CARD]')
    .replace(/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/g, '[REDACTED EMAIL]');
}