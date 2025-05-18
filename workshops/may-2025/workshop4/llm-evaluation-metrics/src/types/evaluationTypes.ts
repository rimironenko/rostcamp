// Interface for accuracy evaluation examples
export interface EvalExample {
  input: string;  // Question or prompt
  ideal: string;  // Expected answer
}

// Interface for bias evaluation examples
export interface BiasEvalExample {
  prompt: string;     // Base prompt for evaluation
  targetGroups: string[];  // Groups to test for bias (e.g., men, women)
  attribute: string;  // Attribute to test (e.g., occupation:doctor)
}

// Results from accuracy evaluation
export interface AccuracyResult {
  accuracyScore: number;
  detailedResults: Array<{
    input: string;
    ideal: string;
    output: string;
    isCorrect: boolean;
  }>;
}

// Results from bias evaluation
export interface BiasResult {
  parityDifferences: Record<string, number>;
  meanAbsoluteParityDifference: number;
  normalizedParityScore: number;
  detailedResults: Array<{
    attribute: string;
    group: string;
    prompt: string;
    response: string;
    associationScore: number;
  }>;
}

// Results from advanced bias evaluation
export interface AdvancedBiasResult {
  biasScores: Record<string, Record<string, number>>;
  effectSizes: Record<string, number>;
  meanAbsoluteEffectSize: number;
  normalizedBiasScore: number;
  detailedResults: Array<{
    attribute: string;
    effectSize: number;
    interpretation: string;
  }>;
}