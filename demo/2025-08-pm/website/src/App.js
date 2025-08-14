import React, { useState, useEffect } from 'react';
import Auth from './components/Auth';
import ChatInterface from './components/ChatInterface';
import { config } from './config';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [theme, setTheme] = useState(() => {
    const savedTheme = localStorage.getItem('theme');
    return savedTheme || config.settings.defaultTheme;
  });

  useEffect(() => {
    // Check if user is already authenticated
    const authStatus = localStorage.getItem('isAuthenticated');
    if (authStatus === 'true') {
      setIsAuthenticated(true);
    }
    
    // Apply theme to document
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    localStorage.removeItem('isAuthenticated');
  };

  if (!isAuthenticated) {
    return (
      <div className="app" data-theme={theme}>
        <Auth onLogin={handleLogin} />
      </div>
    );
  }

  return (
    <div className="app" data-theme={theme}>
      <ChatInterface />
    </div>
  );
}

export default App; 