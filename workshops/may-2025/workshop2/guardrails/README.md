# OpenAI TypeScript Project with Guardrails

A TypeScript application that demonstrates how to use the OpenAI API in a Node.js environment with prompt testing and validation guardrails.

## Features

- TypeScript configuration optimized for Node.js
- OpenAI API integration with prompt templates
- Content validation guardrails for safe AI responses
- Schema validation for structured outputs
- Unit and integration testing framework
- Environment variable management with dotenv
- NPM scripts for development, testing, and building

## Prerequisites

- Node.js (v16 or newer)
- npm or yarn
- OpenAI API key

## Installation

1. Clone the repository (if you haven't already)
2. Navigate to the project directory
3. Install dependencies:

```bash
npm install
```

## Configuration

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Edit the `.env` file and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

You can obtain an API key from your [OpenAI dashboard](https://platform.openai.com/account/api-keys).

## Usage

### Development

To run the application in development mode with auto-reloading:

```bash
npm run dev
```

### Running the application

To start the application:

```bash
npm start
```

### Testing prompt templates with guardrails

To validate a prompt template against the guardrails:

```bash
npm run validate productDescription "Wireless noise-cancelling headphones"
```

### Running tests

To run all tests:

```bash
npm test
```

To run only unit tests (without API calls):

```bash
npm test -- --testPathIgnorePatterns=integration
```

### Linting

To check code quality:

```bash
npm run lint
```

### Building and Type Checking

To compile TypeScript to JavaScript:

```bash
npm run build
```

The compiled JavaScript will be in the `dist` directory.

## Project Structure

```
.
├── src/                    # Source directory
│   ├── config/             # Configuration files
│   │   ├── openai.ts       # OpenAI client configuration
│   │   ├── prompt-types.ts # Type definitions for prompts
│   │   └── prompt-templates.ts # Prompt template definitions
│   ├── guardrails/         # Content validation guardrails
│   │   ├── common-guardrails.ts # Reusable guardrails
│   │   └── validator.ts    # Response validation logic
│   ├── services/           # Service layer
│   │   └── openai-service.ts # OpenAI API service
│   ├── utils/              # Utility functions
│   │   └── validate-prompt.ts # CLI validation utility
│   └── index.ts            # Main application entry point
├── dist/                   # Compiled JavaScript (generated)
├── __tests__/              # Jest test files
├── .env                    # Environment variables (create from .env.example)
├── .env.example            # Example environment file
├── .eslintrc.js            # ESLint configuration
├── .gitignore              # Git ignore file
├── jest.config.js          # Jest configuration
├── package.json            # NPM package configuration
├── tsconfig.json           # TypeScript configuration
└── README.md               # This documentation
```

## Working with Prompt Templates

Prompt templates are defined in `src/config/prompt-templates.ts`. You can create new templates with specific validation rules:

```typescript
const myCustomTemplate: PromptTemplate = {
  name: 'my_template',
  systemPrompt: 'Your system instructions here',
  userPromptTemplate: 'Your user message template with {input} placeholder',
  expectedResponseSchema: z.object({
    // Define expected response schema using Zod
    field1: z.string(),
    field2: z.number(),
  }),
  guardrails: [
    // Add guardrails from common-guardrails.ts or create custom ones
    harmfulContentGuardrail,
    piiGuardrail,
    // Custom guardrail
    {
      name: 'custom_check',
      description: 'Check for custom requirements',
      severity: 'warning',
      check: (response) => !response.includes('unwanted text')
    }
  ]
};
```

## Creating Custom Guardrails

You can create custom guardrails in `src/guardrails/common-guardrails.ts` or directly in your template definition:

```typescript
const myCustomGuardrail: GuardrailConfig = {
  name: 'custom_guardrail',
  description: 'Checks for specific requirements',
  severity: 'error', // 'error' or 'warning'
  check: (response: string): boolean => {
    // Implement your check logic here
    return !response.includes('problematic content');
  }
};
```

## License

ISC

## Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Node.js Documentation](https://nodejs.org/en/docs/)