import { z } from 'zod';
import type { PromptTemplate } from './prompt-types';
import { commonGuardrails, featureHallucinationGuardrail } from '../guardrails/common-guardrails';

// Example schema for product description responses
const productDescriptionSchema = z.object({
  title: z.string().min(3).max(100),
  description: z.string().min(50).max(1000),
  keyFeatures: z.array(z.string()).min(3).max(10),
  targetAudience: z.string().optional(),
});

// Example prompt templates

export const productDescriptionTemplate: PromptTemplate = {
  name: 'product_description',
  systemPrompt: `You are an AI assistant specialized in creating compelling product descriptions. 
  Your job is to create engaging, accurate, and professional product descriptions.
  Always focus on benefits, not just features.
  Never invent features that aren't mentioned in the input.
  Format your response as JSON with the fields: title, description, keyFeatures (array), and optionally targetAudience. 
  Do not wrap the json codes in JSON markers.`,
  userPromptTemplate: `Create a product description for the following product: {input}`,
  expectedResponseSchema: productDescriptionSchema,
  guardrails: [
    ...commonGuardrails,
    featureHallucinationGuardrail
  ]
};

export const contentModerationTemplate: PromptTemplate = {
  name: 'content_moderation',
  systemPrompt: `You are a content moderation assistant. Your job is to review text and flag any potentially inappropriate content.
  Respond with a summary of any issues found or confirm the content is appropriate.
  Be vigilant for harmful, offensive, illegal, or dangerous content.
  Do not repeat explicitly harmful content in your response.`,
  userPromptTemplate: `Please review the following content and provide feedback on its appropriateness: {input}`,
  guardrails: commonGuardrails,
};

// Export all templates
export const templates = {
  productDescription: productDescriptionTemplate,
  contentModeration: contentModerationTemplate,
};