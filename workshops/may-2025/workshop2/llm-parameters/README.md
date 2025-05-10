# OpenAI API Parameter Demonstration

This project demonstrates how different OpenAI API parameters (Temperature, Top P) affect the model's responses. It focuses on a simple single-word completion task to clearly show the impact of each parameter.

## Prerequisites

- Node.js (v16 or newer)
- npm or yarn
- OpenAI API key

## Project Structure

```
src/
├── index.ts            # Main entry point
├── config.ts           # Configuration settings
├── api-client.ts       # OpenAI API client functions
├── parameter-tests.ts  # Individual parameter tests
├── multiple-tests.ts   # Multiple runs with same parameters
└── utils.ts            # Utility functions
```

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   npm install
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

## Available Scripts

The project includes several npm scripts:

- **`npm start`**: Runs the demonstration using ts-node (development mode)
- **`npm run build`**: Compiles TypeScript code to JavaScript in the `dist` directory
- **`npm run run-built`**: Runs the compiled JavaScript code
- **`npm run clean`**: Removes the `dist` directory (added to package.json build step)

## Running the Demonstration

There are two ways to run the demonstration:

### 1. Using ts-node (Development)

```
npm start
```

This runs the TypeScript code directly using ts-node without compiling first.

### 2. Build and Run (Production)

```
npm run build
npm run run-built
```

This first compiles the TypeScript code to JavaScript in the `dist` directory, then runs the compiled code. This is the recommended approach for production use.

Both methods will run the demonstration with the following prompt:

```
"Please finish the sentence (replace the dots in the end): 'It's raining in the city and all people on the street are ...'. Use just 1 word."
```

## What This Demonstration Shows

1. **Parameter Variations**: Tests different Temperature and Top P settings to show how they affect completions.

2. **Consistency vs. Diversity**: Shows how low Temperature/Top P values produce consistent results, while high values generate diverse completions.

3. **Statistical Analysis**: For each parameter set, runs the same prompt multiple times and calculates uniqueness statistics.

## Parameter Configurations Tested

- **Default**: temperature=1.0, top_p=1.0
- **Low Temperature**: temperature=0.2, top_p=1.0
- **High Temperature**: temperature=1.8, top_p=1.0
- **Low Top P**: temperature=1.0, top_p=0.1
- **High Top P**: temperature=1.0, top_p=0.9

## Multiple Run Analysis

For selected parameter sets, the demonstration runs the same prompt multiple times to show:

1. How consistent/varied the outputs are
2. The percentage of unique responses
3. The distribution of different completions

## API Rate Limiting

This project implements a 1-second delay between API calls to avoid rate limiting issues. You can adjust this delay in the `config.ts` file by changing the `API_CALL_DELAY_MS` constant.

## Customizing

To modify the demonstration:

1. **Change the prompt**: Edit the `COMPLETION_PROMPT` constant in `src/index.ts`
2. **Test different parameters**: Modify the configurations in `src/config.ts`
3. **Adjust number of multiple runs**: Change `NUM_MULTIPLE_RUNS` in `src/config.ts`
4. **Modify API delay**: Change `API_CALL_DELAY_MS` in `src/config.ts`

## Understanding the Results

- **Low temperature/top_p**: Will produce very consistent responses (often the same word each time)
- **Default settings**: Provide a balance of consistency and variety
- **High temperature/top_p**: Generate diverse and sometimes unexpected completions