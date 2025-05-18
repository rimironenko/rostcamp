/**
 * src/utils/fileUtils.ts
 * Utilities for file operations
 */

import * as fs from 'fs/promises';
import * as path from 'path';

/**
 * Saves data to a JSON file
 * @param filename Name of the file to save
 * @param data Data to save
 */
export async function saveResults(filename: string, data: any) {
  try {
    const resultsDir = path.join(process.cwd(), 'results');
    
    // Create results directory if it doesn't exist
    try {
      await fs.access(resultsDir);
    } catch {
      await fs.mkdir(resultsDir, { recursive: true });
    }
    
    const filePath = path.join(resultsDir, filename);
    
    await fs.writeFile(
      filePath,
      JSON.stringify(data, null, 2)
    );
    
    console.log(`Results saved to ${filePath}`);
  } catch (error) {
    console.error(`Error saving results to ${filename}:`, error);
  }
}