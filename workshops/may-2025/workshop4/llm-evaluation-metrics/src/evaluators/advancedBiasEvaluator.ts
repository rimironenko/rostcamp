/**
 * src/evaluators/advancedBiasEvaluator.ts
 * Implements a more advanced bias detection approach inspired by WEAT (Word Embedding Association Test)
 */

import { openai } from '../utils/openaiClient';
import { BiasEvalExample, AdvancedBiasResult } from '../types/evaluationTypes';
import { getBiasExamples } from '../data/biasExamples';

/**
 * Gets embedding vectors for a list of terms
 * @param terms List of terms to get embeddings for
 * @returns Object mapping terms to their embedding vectors
 */
async function getEmbeddings(terms: string[]): Promise<Record<string, number[]>> {
  const result: Record<string, number[]> = {};
  
  for (const term of terms) {
    try {
      const response = await openai.embeddings.create({
        model: "text-embedding-ada-002",
        input: term,
      });
      
      result[term] = response.data[0].embedding;
    } catch (error) {
      console.error(`Error getting embedding for term ${term}:`, error);
    }
  }
  
  return result;
}

/**
 * Calculates cosine similarity between two vectors
 * @param vector1 First vector
 * @param vector2 Second vector
 * @returns Cosine similarity score between -1 and 1
 */
function cosineSimilarity(vector1: number[], vector2: number[]): number {
  if (vector1.length !== vector2.length) {
    throw new Error("Vectors must have the same length");
  }
  
  let dotProduct = 0;
  let magnitude1 = 0;
  let magnitude2 = 0;
  
  for (let i = 0; i < vector1.length; i++) {
    dotProduct += vector1[i] * vector2[i];
    magnitude1 += vector1[i] * vector1[i];
    magnitude2 += vector2[i] * vector2[i];
  }
  
  magnitude1 = Math.sqrt(magnitude1);
  magnitude2 = Math.sqrt(magnitude2);
  
  if (magnitude1 === 0 || magnitude2 === 0) {
    return 0;
  }
  
  return dotProduct / (magnitude1 * magnitude2);
}

/**
 * Calculates bias scores using embedding association tests
 * @param attributeEmbeddings Embeddings for attribute terms
 * @param targetGroupEmbeddings Embeddings for target group terms
 * @returns Object with bias association scores
 */
function calculateBiasScores(
  attributeEmbeddings: Record<string, number[]>,
  targetGroupEmbeddings: Record<string, number[]>
): Record<string, Record<string, number>> {
  const biasScores: Record<string, Record<string, number>> = {};
  
  for (const attribute in attributeEmbeddings) {
    biasScores[attribute] = {};
    const attributeVector = attributeEmbeddings[attribute];
    
    for (const group in targetGroupEmbeddings) {
      const groupVector = targetGroupEmbeddings[group];
      biasScores[attribute][group] = cosineSimilarity(attributeVector, groupVector);
    }
  }
  
  return biasScores;
}

/**
 * Calculates effect size (Cohen's d) between two groups for each attribute
 * @param biasScores Object with bias association scores
 * @returns Object with effect sizes
 */
function calculateEffectSizes(
  biasScores: Record<string, Record<string, number>>
): Record<string, number> {
  const effectSizes: Record<string, number> = {};
  
  for (const attribute in biasScores) {
    const scores = biasScores[attribute];
    const groups = Object.keys(scores);
    
    if (groups.length < 2) {
      effectSizes[attribute] = 0;
      continue;
    }
    
    // Calculate effect size (simplified for two groups)
    const group1 = groups[0];
    const group2 = groups[1];
    const diff = scores[group1] - scores[group2];
    
    // Normalize to -1 to 1 range
    effectSizes[attribute] = Math.max(-1, Math.min(1, diff));
  }
  
  return effectSizes;
}

/**
 * Advanced bias evaluation using embedding association tests
 */
export async function evaluateAdvancedBias(): Promise<AdvancedBiasResult> {
  console.log("Starting advanced bias evaluation...");
  
  // Get examples from our dataset
  const biasExamples: BiasEvalExample[] = getBiasExamples();
  
  // Extract attributes and target groups
  const attributes: string[] = [...new Set(biasExamples.map(example => 
    example.attribute.split(':')[1]
  ))];
  
  const targetGroups: string[] = [...new Set(
    biasExamples.flatMap(example => example.targetGroups)
  )];
  
  console.log(`Testing ${attributes.length} attributes across ${targetGroups.length} groups`);
  
  // Get embeddings for attributes and target groups
  console.log("Getting embeddings for attributes...");
  const attributeEmbeddings = await getEmbeddings(attributes);
  
  console.log("Getting embeddings for target groups...");
  const targetGroupEmbeddings = await getEmbeddings(targetGroups);
  
  // Calculate bias scores
  console.log("Calculating bias scores...");
  const biasScores = calculateBiasScores(attributeEmbeddings, targetGroupEmbeddings);
  
  // Calculate effect sizes
  console.log("Calculating effect sizes...");
  const effectSizes = calculateEffectSizes(biasScores);
  
  // Calculate overall bias score (mean absolute effect size)
  const totalEffectSize = Object.values(effectSizes).reduce(
    (sum, size) => sum + Math.abs(size), 
    0
  );
  const meanAbsoluteEffectSize = totalEffectSize / Object.keys(effectSizes).length;
  
  // Calculate normalized bias score (0 = highly biased, 1 = neutral)
  const normalizedBiasScore = 1 - meanAbsoluteEffectSize;
  
  console.log(`Advanced Bias Evaluation Complete:`);
  console.log(`Mean Absolute Effect Size = ${meanAbsoluteEffectSize.toFixed(4)}`);
  console.log(`Normalized Bias Score (1 is neutral, 0 is biased): ${normalizedBiasScore.toFixed(4)}`);
  
  return {
    biasScores,
    effectSizes,
    meanAbsoluteEffectSize,
    normalizedBiasScore,
    detailedResults: Object.entries(effectSizes).map(([attribute, effectSize]) => ({
      attribute,
      effectSize,
      interpretation: interpretEffectSize(effectSize, attribute, targetGroups),
    })),
  };
}

/**
 * Provides an interpretation of the effect size
 * @param effectSize Cohen's d effect size
 * @param attribute The attribute being evaluated
 * @param groups The target groups
 * @returns Human-readable interpretation
 */
function interpretEffectSize(effectSize: number, attribute: string, groups: string[]): string {
  const absEffect = Math.abs(effectSize);
  let magnitude = "no";
  
  if (absEffect >= 0.8) magnitude = "very strong";
  else if (absEffect >= 0.5) magnitude = "strong";
  else if (absEffect >= 0.2) magnitude = "moderate";
  else if (absEffect > 0.1) magnitude = "small";
  
  if (absEffect <= 0.1) {
    return `No significant bias detected for ${attribute} between ${groups.join(" and ")}.`;
  }
  
  const favoredGroup = effectSize > 0 ? groups[0] : groups[1];
  
  return `${magnitude} bias detected for ${attribute}, favoring ${favoredGroup}.`
}