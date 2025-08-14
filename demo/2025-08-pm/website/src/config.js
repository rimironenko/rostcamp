// Configuration file for ChatGPT Lambda Website
// Update these values as needed without requiring rebuild

export const config = {
  // Basic authentication credentials
  auth: {
    username: "admin",
    password: "password123"
  },
  
  // AWS Lambda function URL
  lambdaUrl: "https://your-lambda-function-url.lambda-url.us-east-1.on.aws/",
  
  // Application settings
  settings: {
    maxInputLength: 1000,
    defaultTheme: "dark" // "light" or "dark"
  }
};

export default config; 