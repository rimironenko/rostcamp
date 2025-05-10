/**
 * Utility functions for the OpenAI parameter demonstration
 */

/**
 * Format a number to a fixed number of decimal places
 */
export function formatNumber(value: number, decimals: number = 1): string {
  return value.toFixed(decimals);
}

/**
 * Calculate the mean of an array of numbers
 */
export function calculateMean(values: number[]): number {
  if (values.length === 0) return 0;
  const sum = values.reduce((a, b) => a + b, 0);
  return sum / values.length;
}

/**
 * Calculate the standard deviation of an array of numbers
 */
export function calculateStandardDeviation(values: number[]): number {
  if (values.length <= 1) return 0;
  
  const mean = calculateMean(values);
  const squareDiffs = values.map(value => Math.pow(value - mean, 2));
  const avgSquareDiff = calculateMean(squareDiffs);
  
  return Math.sqrt(avgSquareDiff);
}

/**
 * Create a histogram of responses
 */
export function createHistogram(responses: string[]): Record<string, number> {
  const histogram: Record<string, number> = {};
  
  for (const response of responses) {
    histogram[response] = (histogram[response] || 0) + 1;
  }
  
  // Sort by frequency
  const sortedHistogram: Record<string, number> = {};
  Object.entries(histogram)
    .sort((a, b) => b[1] - a[1])
    .forEach(([key, value]) => {
      sortedHistogram[key] = value;
    });
  
  return sortedHistogram;
}

/**
 * Format a histogram for display
 */
export function formatHistogram(histogram: Record<string, number>, totalCount: number): string {
  let result = '';
  
  Object.entries(histogram).forEach(([response, count]) => {
    const percentage = (count / totalCount) * 100;
    result += `  ${response}: ${count} (${percentage.toFixed(1)}%)\n`;
  });
  
  return result;
}