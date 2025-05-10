// Direct type definitions for prompt templates
import { z } from 'zod';

export interface PromptTemplate {
  name: string;
  systemPrompt: string;
  userPromptTemplate: string;
  expectedResponseSchema?: z.ZodType<any>;
  guardrails?: GuardrailConfig[];
}

export interface GuardrailConfig {
  name: string;
  description: string;
  check: (response: string) => boolean | Promise<boolean>;
  severity: 'warning' | 'error';
}

export interface ValidationResult {
  isValid: boolean;
  errors: ValidationError[];
  warnings: ValidationWarning[];
  rawResponse: string;
  processedResponse?: any;
}

export interface ValidationError {
  guardrail: string;
  message: string;
}

export interface ValidationWarning {
  guardrail: string;
  message: string;
}