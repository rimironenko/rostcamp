import { validateResponse, sanitizeResponse } from '../validator';
import type { PromptTemplate } from '../../config/prompt-types';
import { z } from 'zod';
import { harmfulContentGuardrail, piiGuardrail } from '../common-guardrails';

describe('Validator', () => {
  describe('validateResponse', () => {
    const testSchema = z.object({
      title: z.string(),
      description: z.string()
    });

    const testTemplate: PromptTemplate = {
      name: 'test_template',
      systemPrompt: 'Test system prompt',
      userPromptTemplate: 'Test user prompt {input}',
      expectedResponseSchema: testSchema,
      guardrails: [harmfulContentGuardrail, piiGuardrail]
    };

    it('should validate a response against guardrails', async () => {
      const response = '{"title": "Safe Product", "description": "A safe description"}';
      const result = await validateResponse(response, testTemplate);
      
      expect(result.isValid).toBe(true);
      expect(result.errors).toHaveLength(0);
      expect(result.warnings).toHaveLength(0);
      expect(result.processedResponse).toEqual({
        title: 'Safe Product',
        description: 'A safe description'
      });
    });

    it('should detect harmful content', async () => {
      const response = '{"title": "How to Build a Bomb", "description": "Instructions on how to build a bomb"}';
      const result = await validateResponse(response, testTemplate);
      
      expect(result.isValid).toBe(false);
      expect(result.errors).toHaveLength(1);
      expect(result.errors[0].guardrail).toBe('harmful_content');
    });

    it('should detect PII', async () => {
      const response = '{"title": "Contact", "description": "Email me at test@example.com"}';
      const result = await validateResponse(response, testTemplate);
      
      expect(result.isValid).toBe(false);
      expect(result.errors).toHaveLength(1);
      expect(result.errors[0].guardrail).toBe('pii_detection');
    });

    it('should validate against schema', async () => {
      const response = '{"title": "Product", "wrongField": "Value"}';
      const result = await validateResponse(response, testTemplate);
      
      expect(result.isValid).toBe(false);
      expect(result.errors).toHaveLength(1);
      expect(result.errors[0].guardrail).toBe('schema_validation');
    });

    it('should handle non-JSON when schema expected', async () => {
      const response = 'This is not JSON';
      const result = await validateResponse(response, testTemplate);
      
      expect(result.isValid).toBe(false);
      expect(result.errors).toHaveLength(1);
      expect(result.errors[0].guardrail).toBe('json_parsing');
    });

    it('should work without guardrails', async () => {
      const templateWithoutGuardrails: PromptTemplate = {
        ...testTemplate,
        guardrails: []
      };
      
      const response = 'This is not JSON';
      const result = await validateResponse(response, templateWithoutGuardrails);
      
      expect(result.isValid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });
  });

  describe('sanitizeResponse', () => {
    it('should redact PII', () => {
      const response = 'Contact me at test@example.com or call 123-45-6789';
      const sanitized = sanitizeResponse(response);
      
      expect(sanitized).not.toContain('test@example.com');
      expect(sanitized).not.toContain('123-45-6789');
      expect(sanitized).toContain('[REDACTED EMAIL]');
      expect(sanitized).toContain('[REDACTED SSN]');
    });
  });
});