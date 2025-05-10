/**
 * Configuration for the OpenAI API parameter demonstration
 */

import { OpenAI } from 'openai';
import dotenv from 'dotenv';

dotenv.config();

// Define parameter configurations to test
export interface ParameterConfig {
  name: string;
  temperature?: number;
  top_p?: number;
  description: string;
}

// Initialize the OpenAI client
export const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Parameter configurations for individual tests
export const parameterConfigs: ParameterConfig[] = [
  {
    name: "Default",
    temperature: 1.0,
    top_p: 1.0,
    description: "Default settings (temperature=1.0, top_p=1.0). Balanced randomness."
  },
  {
    name: "Low Temperature",
    temperature: 0.2,
    top_p: 1.0,
    description: "Low temperature (0.2) produces more focused, deterministic responses."
  },
  {
    name: "High Temperature",
    temperature: 2.0,
    top_p: 1.0,
    description: "High temperature (1.8) produces more random, creative, and diverse responses."
  },
  {
    name: "Low Top P",
    temperature: 1.0,
    top_p: 0.1,
    description: "Low top_p (0.1) considers only the most likely tokens, giving more focused responses."
  },
  {
    name: "High Top P",
    temperature: 1.0,
    top_p: 0.9,
    description: "High top_p (0.9) considers more potential tokens, increasing diversity."
  }
];

// Configuration for multiple runs with the same parameters
export const multiRunConfigs: ParameterConfig[] = [
  { 
    name: "Default (temperature=1.0, top_p=1.0)", 
    temperature: 1.0, 
    top_p: 1.0,
    description: "Default settings with balanced randomness."
  },
  { 
    name: "Low Temperature (temperature=0.2, top_p=1.0)", 
    temperature: 0.2, 
    top_p: 1.0,
    description: "Low temperature for deterministic responses."
  },
  { 
    name: "High Temperature (temperature=1.8, top_p=1.0)", 
    temperature: 1.8, 
    top_p: 1.0,
    description: "High temperature for maximum diversity."
  }
];

// Common parameters for OpenAI API calls
export const DEFAULT_MODEL = "gpt-4o";
export const SYSTEM_PROMPT = "You are a helpful assistant.";
export const NUM_MULTIPLE_RUNS = 10;
export const MAX_COMPLETION_TOKENS = 500;

// Delay configuration
export const API_CALL_DELAY_MS = 1000; // 1 second delay between API calls