# OpenAI TypeScript Project

A TypeScript application that demonstrates how to use the OpenAI API in a Node.js environment.

## Features

- TypeScript configuration optimized for Node.js
- OpenAI API integration
- Environment variable management with dotenv
- NPM scripts for development and building

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

### Building for production

To compile TypeScript to JavaScript:

```bash
npm run build
```

The compiled JavaScript will be in the `dist` directory.

## Project Structure

```
.
├── src/                # Source directory
│   └── index.ts        # Main application entry point
├── dist/               # Compiled JavaScript (generated)
├── .env                # Environment variables (create from .env.example)
├── .env.example        # Example environment file
├── .gitignore          # Git ignore file
├── package.json        # NPM package configuration
├── tsconfig.json       # TypeScript configuration
└── README.md           # This documentation
```

## Customizing API Calls

The main OpenAI API call is in `src/index.ts`. You can modify this file to change the model, prompt, temperature, and other parameters:

```typescript
const completion = await openai.chat.completions.create({
  model: "gpt-4",           // Change the model here
  messages: [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "Hello, world!" }  // Change the prompt here
  ],
  // Add other parameters like temperature, max_tokens, etc.
});
```

## License

ISC

## Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Node.js Documentation](https://nodejs.org/en/docs/)