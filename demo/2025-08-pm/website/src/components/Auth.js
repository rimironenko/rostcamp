import React, { useState } from 'react';
import { config } from '../config';
import { Lock, User, Eye, EyeOff } from 'lucide-react';
import './Auth.css';

const Auth = ({ onLogin }) => {
  const [credentials, setCredentials] = useState({
    username: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    if (credentials.username === config.auth.username && 
        credentials.password === config.auth.password) {
      localStorage.setItem('isAuthenticated', 'true');
      onLogin();
    } else {
      setError('Invalid username or password');
    }
  };

  const handleChange = (e) => {
    setCredentials({
      ...credentials,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <Lock className="auth-icon" />
          <h1>Login Required</h1>
          <p>Please enter your credentials to access the ChatGPT interface</p>
        </div>
        
        <form onSubmit={handleSubmit} className="auth-form">
          <div className="input-group">
            <div className="input-wrapper">
              <User className="input-icon" />
              <input
                type="text"
                name="username"
                placeholder="Username"
                value={credentials.username}
                onChange={handleChange}
                className="auth-input"
                required
              />
            </div>
          </div>
          
          <div className="input-group">
            <div className="input-wrapper">
              <Lock className="input-icon" />
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                placeholder="Password"
                value={credentials.password}
                onChange={handleChange}
                className="auth-input"
                required
              />
              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
          </div>
          
          {error && <div className="auth-error">{error}</div>}
          
          <button type="submit" className="auth-button">
            Login
          </button>
        </form>
        
        <div className="auth-footer">
          <small>Default credentials: admin / password123</small>
        </div>
      </div>
    </div>
  );
};

export default Auth; 