import { OpenAI } from 'openai';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

// Validate API key exists
if (!process.env.OPENAI_API_KEY) {
  throw new Error('OPENAI_API_KEY is not defined in environment variables');
}

// Create and export the OpenAI client
export const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Default models configuration
export const MODELS = {
  DEFAULT: 'gpt-4o',
  FALLBACK: 'gpt-4',
};

// Default parameters
export const DEFAULT_PARAMS = {
  temperature: 0.7,
  max_tokens: 500,
  stream: false, // Explicitly set stream to false to ensure we get a ChatCompletion response
};