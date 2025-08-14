import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { Send, Sun, Moon, Loader2, AlertCircle, X } from 'lucide-react';
import { config } from '../config';
import './ChatInterface.css';

const ChatInterface = () => {
  const [input, setInput] = useState('');
  const [response, setResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [theme, setTheme] = useState(() => {
    const savedTheme = localStorage.getItem('theme');
    return savedTheme || config.settings.defaultTheme;
  });
  const [inputHistory, setInputHistory] = useState(() => {
    const saved = localStorage.getItem('inputHistory');
    return saved ? JSON.parse(saved) : [];
  });
  
  const inputRef = useRef(null);
  const responseRef = useRef(null);

  // Apply theme to document
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  // Save input history to localStorage
  useEffect(() => {
    localStorage.setItem('inputHistory', JSON.stringify(inputHistory));
  }, [inputHistory]);

  // Auto-resize textarea
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.style.height = 'auto';
      inputRef.current.style.height = Math.min(inputRef.current.scrollHeight, 200) + 'px';
    }
  }, [input]);

  // Scroll to response when it appears
  useEffect(() => {
    if (response && responseRef.current) {
      responseRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [response]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!input.trim() || isLoading) return;
    
    const trimmedInput = input.trim();
    if (trimmedInput.length > config.settings.maxInputLength) {
      setError(`Input too long. Maximum ${config.settings.maxInputLength} characters allowed.`);
      return;
    }

    setIsLoading(true);
    setError('');
    setResponse('');

    try {
      const response = await fetch(config.lambdaUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: trimmedInput }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.genai_response) {
        setResponse(data.genai_response);
        // Add to input history
        setInputHistory(prev => {
          const newHistory = [trimmedInput, ...prev.slice(0, 9)]; // Keep last 10 inputs
          return newHistory;
        });
      } else {
        throw new Error('Invalid response format from Lambda function');
      }
    } catch (err) {
      setError(`Error: ${err.message}. Please check your Lambda function URL and CORS configuration.`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  const clearError = () => {
    setError('');
  };

  const clearResponse = () => {
    setResponse('');
  };

  const characterCount = input.length;
  const isOverLimit = characterCount > config.settings.maxInputLength;

  return (
    <div className="chat-container">
      {/* Header */}
      <header className="chat-header">
        <div className="header-content">
          <h1>ChatGPT Lambda Interface</h1>
          <button onClick={toggleTheme} className="theme-toggle">
            {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
          </button>
        </div>
      </header>

      {/* Main Chat Area */}
      <main className="chat-main">
        <div className="chat-content">
          {/* Response Area */}
          {response && (
            <div className="response-container" ref={responseRef}>
              <div className="response-header">
                <span className="response-label">Response:</span>
                <button onClick={clearResponse} className="clear-button">
                  <X size={16} />
                </button>
              </div>
              <div className="response-content">
                <ReactMarkdown
                  components={{
                    code({ node, inline, className, children, ...props }) {
                      const match = /language-(\w+)/.exec(className || '');
                      return !inline && match ? (
                        <pre className="code-block">
                          <code className={className} {...props}>
                            {children}
                          </code>
                        </pre>
                      ) : (
                        <code className="inline-code" {...props}>
                          {children}
                        </code>
                      );
                    }
                  }}
                >
                  {response}
                </ReactMarkdown>
              </div>
            </div>
          )}

          {/* Loading State */}
          {isLoading && (
            <div className="loading-container">
              <Loader2 className="loading-spinner" />
              <p>Processing your request...</p>
            </div>
          )}

          {/* Error Display */}
          {error && (
            <div className="error-container">
              <div className="error-header">
                <AlertCircle className="error-icon" />
                <span>Error</span>
                <button onClick={clearError} className="clear-button">
                  <X size={16} />
                </button>
              </div>
              <p>{error}</p>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="input-container">
          <form onSubmit={handleSubmit} className="input-form">
            <div className="input-wrapper">
              <textarea
                ref={inputRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message here... (Press Enter to send, Shift+Enter for new line)"
                className={`chat-input ${isOverLimit ? 'input-error' : ''}`}
                disabled={isLoading}
                maxLength={config.settings.maxInputLength}
              />
              <div className="input-footer">
                <span className={`character-count ${isOverLimit ? 'count-error' : ''}`}>
                  {characterCount}/{config.settings.maxInputLength}
                </span>
                <button
                  type="submit"
                  disabled={!input.trim() || isLoading || isOverLimit}
                  className="send-button"
                >
                  {isLoading ? (
                    <Loader2 className="send-spinner" />
                  ) : (
                    <Send size={20} />
                  )}
                </button>
              </div>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
};

export default ChatInterface; 