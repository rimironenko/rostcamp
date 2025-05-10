import { OpenAI } from 'openai';
import dotenv from 'dotenv';

dotenv.config();

// Initialize the OpenAI client
// You should use environment variables for the API key in production
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY, // This reads from the .env file or environment variables
});

async function main() {
  try {
    const completion = await openai.chat.completions.create({
      model: "gpt-4",
      messages: [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: "Hello, world!" }
      ],
    });

    console.log("Response:", completion.choices[0].message.content);
  } catch (error) {
    console.error("Error:", error);
  }
}

main();