import nock from 'nock';
import { OpenAIService } from '../openai-service';
import type { PromptTemplate } from '../../config/prompt-types';

// Mock OpenAI API responses
jest.mock('../../config/openai', () => ({
  openai: {
    chat: {
      completions: {
        create: jest.fn()
      }
    }
  },
  MODELS: {
    DEFAULT: 'gpt-4',
    FALLBACK: 'gpt-3.5-turbo'
  },
  DEFAULT_PARAMS: {
    temperature: 0.7,
    max_tokens: 500
  }
}));

// Import the mocked module
import { openai } from '../../config/openai';

describe('OpenAIService', () => {
  let service: OpenAIService;
  
  const mockTemplate: PromptTemplate = {
    name: 'test_template',
    systemPrompt: 'You are a helpful assistant',
    userPromptTemplate: 'Answer the following: {input}',
    guardrails: []
  };

  beforeEach(() => {
    service = new OpenAIService();
    jest.resetAllMocks();
  });

  afterEach(() => {
    nock.cleanAll();
  });

  it('should call OpenAI API with correct parameters', async () => {
    // Mock the OpenAI API response
    (openai.chat.completions.create as jest.Mock).mockResolvedValueOnce({
      choices: [
        {
          message: {
            content: 'This is a test response'
          }
        }
      ]
    });

    await service.promptWithGuardrails(mockTemplate, 'test question');

    // Verify API was called with correct parameters
    expect(openai.chat.completions.create).toHaveBeenCalledWith(
      expect.objectContaining({
        model: 'gpt-4',
        messages: [
          { role: 'system', content: 'You are a helpful assistant' },
          { role: 'user', content: 'Answer the following: test question' }
        ]
      })
    );
  });

  it('should handle API errors', async () => {
    // Mock an API error
    (openai.chat.completions.create as jest.Mock).mockRejectedValueOnce(
      new Error('API Error')
    );

    await expect(
      service.promptWithGuardrails(mockTemplate, 'test question')
    ).rejects.toThrow('API Error');
  });

  it('should fall back to alternative model when primary fails', async () => {
    // Mock first call to fail, second to succeed
    (openai.chat.completions.create as jest.Mock)
      .mockRejectedValueOnce(new Error('API Error'))
      .mockResolvedValueOnce({
        choices: [
          {
            message: {
              content: 'Fallback response'
            }
          }
        ]
      });

    const result = await service.promptWithFallback(mockTemplate, 'test question');

    // Verify fallback was called
    expect(openai.chat.completions.create).toHaveBeenCalledTimes(2);
    expect(openai.chat.completions.create).toHaveBeenLastCalledWith(
      expect.objectContaining({
        model: 'gpt-3.5-turbo'
      })
    );
    expect(result.rawResponse).toBe('Fallback response');
  });
});