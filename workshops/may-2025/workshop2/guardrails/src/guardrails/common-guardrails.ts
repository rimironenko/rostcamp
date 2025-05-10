import type { GuardrailConfig } from '../config/prompt-types';

// Collection of common guardrails that can be reused across different prompts

/**
 * Check for potentially harmful content
 */
export const harmfulContentGuardrail: GuardrailConfig = {
  name: 'harmful_content',
  description: 'Checks for potentially harmful or malicious content',
  severity: 'error',
  check: (response: string): boolean => {
    const harmfulPatterns = [
      /how to (make|create|build) (bomb|explosive|weapon)/i,
      /(hack|compromise|break into) (password|account|system)/i,
      /(illegal|illicit) (drug|substance) (creation|manufacturing|synthesis)/i,
      // Add more patterns as needed
    ];

    return !harmfulPatterns.some(pattern => pattern.test(response));
  }
};

/**
 * Check for potentially personally identifiable information (PII)
 */
export const piiGuardrail: GuardrailConfig = {
  name: 'pii_detection',
  description: 'Checks for personally identifiable information',
  severity: 'error',
  check: (response: string): boolean => {
    const piiPatterns = [
      /\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b/, // SSN
      /\b\d{16}\b/, // Credit card numbers (simplified)
      /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/, // Email
      // Add more patterns as needed
    ];

    return !piiPatterns.some(pattern => pattern.test(response));
  }
};

/**
 * Check for response length to avoid excessive tokens
 */
export const responseLengthGuardrail: GuardrailConfig = {
  name: 'response_length',
  description: 'Ensures response is not excessively long',
  severity: 'warning',
  check: (response: string): boolean => {
    // Approximate token count (rough estimate)
    const tokenCount = response.split(/\s+/).length;
    return tokenCount < 1000; // Warning if more than ~1000 tokens
  }
};

/**
 * Check that the response is formatted correctly, not just raw JSON
 */
export const formattingGuardrail: GuardrailConfig = {
  name: 'formatting',
  description: 'Checks for proper formatting in user-facing responses',
  severity: 'warning',
  check: (response: string): boolean => {
    // Check if response is just raw JSON when it shouldn't be
    const isRawJson = response.trim().startsWith('{') && response.trim().endsWith('}');
    const hasMarkdown = response.includes('```') || response.includes('#');
    
    return !isRawJson || hasMarkdown;
  }
};

/**
 * Ensure responses don't contain hallucinations about features
 */
export const featureHallucinationGuardrail: GuardrailConfig = {
  name: 'feature_hallucination',
  description: 'Checks for hallucinations about non-existent features',
  severity: 'warning',
  check: (response: string): boolean => {
    const disallowedFeatures = [
      /voice recognition/i,
      /video processing/i,
      /real-time analysis/i,
      // Add features that don't exist
    ];

    return !disallowedFeatures.some(pattern => pattern.test(response));
  }
};

// Export a set of common guardrails
export const commonGuardrails = [
  harmfulContentGuardrail,
  piiGuardrail,
  responseLengthGuardrail,
  formattingGuardrail
];