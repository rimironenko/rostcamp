/**
 * src/utils/openaiClient.ts
 * OpenAI client configuration
 */

import { OpenAI } from 'openai';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

// Check if API key is available
if (!process.env.OPENAI_API_KEY) {
  console.error("ERROR: OPENAI_API_KEY environment variable is not set. Please set it before running this application.");
  process.exit(1);
}

// Initialize and export OpenAI client
export const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});