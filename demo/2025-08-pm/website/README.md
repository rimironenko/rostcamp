# ChatGPT Lambda Website

A ChatGPT-like interface that integrates with AWS Lambda functions for AI-powered responses. Built with React and designed for deployment on Amazon S3.

## Features

- 🤖 **ChatGPT-like Interface**: Clean, modern chat interface with markdown rendering
- 🔐 **Basic Authentication**: Configurable login/password protection
- 🌓 **Light/Dark Mode**: Toggle between light and dark themes
- 📱 **Responsive Design**: Mobile-friendly interface
- ⚡ **AWS Lambda Integration**: Direct integration with Lambda function URLs
- 📝 **Input Validation**: 1000 character limit with real-time feedback
- 💾 **Local Storage**: Persistent theme preferences and input history
- 🎨 **Modern UI**: Beautiful, accessible design with smooth animations

## Technical Stack

- **Frontend**: React 18 with static export
- **Styling**: CSS with CSS variables for theming
- **Markdown**: React Markdown with syntax highlighting
- **Icons**: Lucide React
- **Deployment**: Amazon S3 static website hosting
- **Backend**: AWS Lambda function with direct function URL

## Quick Start

### Prerequisites

- Node.js 16+ and npm
- AWS account with Lambda function configured
- Lambda function URL with CORS enabled

### Installation

1. **Clone and install dependencies:**
   ```bash
   npm install
   ```

2. **Configure your Lambda function URL:**
   Edit `src/config.js` and update the `lambdaUrl` with your actual Lambda function URL:
   ```javascript
   lambdaUrl: "https://your-lambda-function-url.lambda-url.us-east-1.on.aws/"
   ```

3. **Update authentication credentials (optional):**
   In `src/config.js`, change the default credentials:
   ```javascript
   auth: {
     username: "your-username",
     password: "your-password"
   }
   ```

4. **Start development server:**
   ```bash
   npm start
   ```

5. **Build for production:**
   ```bash
   npm run build
   ```

## Configuration

The application uses a centralized configuration file (`src/config.js`) that can be updated without rebuilding:

### Authentication Settings
```javascript
auth: {
  username: "admin",        // Login username
  password: "password123"   // Login password
}
```

### Lambda Function Settings
```javascript
lambdaUrl: "https://your-lambda-function-url.lambda-url.us-east-1.on.aws/"
```

### Application Settings
```javascript
settings: {
  maxInputLength: 1000,     // Maximum input characters
  defaultTheme: "dark"      // "light" or "dark"
}
```

## AWS Lambda Function Requirements

Your Lambda function must:

1. **Accept POST requests** with JSON body containing a `prompt` field
2. **Return JSON response** with a `genai_response` field
3. **Have CORS enabled** for cross-origin requests

### Example Lambda Function (Python)
```python
import json

def lambda_handler(event, context):
    # Parse the incoming request
    body = json.loads(event['body'])
    prompt = body.get('prompt', '')
    
    # Your AI processing logic here
    response_text = f"Processed: {prompt}"
    
    # Return the response
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, OPTIONS'
        },
        'body': json.dumps({
            'genai_response': response_text
        })
    }
```

### CORS Configuration
Ensure your Lambda function URL has CORS enabled with these headers:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Headers: Content-Type`
- `Access-Control-Allow-Methods: POST, OPTIONS`

## Deployment to Amazon S3

### 1. Build the Application
```bash
npm run build
```

### 2. Create S3 Bucket
- Create a new S3 bucket
- Enable "Static website hosting"
- Set index document to `index.html`
- Set error document to `index.html` (for React Router)

### 3. Configure Bucket Policy
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::your-bucket-name/*"
        }
    ]
}
```

### 4. Upload Files
Upload all files from the `build/` directory to your S3 bucket.

### 5. Access Your Website
Your website will be available at the S3 static website URL.

## Project Structure

```
src/
├── components/
│   ├── Auth.js              # Authentication component
│   ├── Auth.css             # Auth component styles
│   ├── ChatInterface.js     # Main chat interface
│   └── ChatInterface.css    # Chat interface styles
├── config.js                # Configuration file
├── App.js                   # Main app component
├── App.css                  # App styles
├── index.js                 # React entry point
└── index.css                # Global styles
```

## Features in Detail

### Authentication
- Basic username/password authentication
- Persistent login state using localStorage
- Configurable credentials in config file

### Chat Interface
- Single prompt input with character limit
- Real-time character counting
- Auto-resizing textarea
- Enter to send, Shift+Enter for new line
- Loading spinner during requests
- Error handling with dismissible alerts

### Markdown Rendering
- Full markdown support for responses
- Syntax highlighting for code blocks
- Inline code formatting
- Lists, headers, blockquotes, and more

### Theme System
- Light and dark mode toggle
- Persistent theme preference
- Smooth transitions between themes
- CSS variables for easy customization

### Responsive Design
- Mobile-first approach
- Responsive layout for all screen sizes
- Touch-friendly interface
- Optimized for mobile devices

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure your Lambda function has proper CORS headers
2. **Authentication Issues**: Check credentials in `src/config.js`
3. **Build Errors**: Ensure all dependencies are installed with `npm install`
4. **Lambda Timeout**: Increase Lambda function timeout if responses are slow

### Debug Mode
To enable debug logging, add this to your browser console:
```javascript
localStorage.setItem('debug', 'true');
```

## Security Considerations

- This implementation uses basic authentication stored in localStorage
- For production use, consider implementing proper session management
- Lambda function URLs should be secured with appropriate IAM policies
- Consider using AWS Cognito for more robust authentication

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review AWS Lambda documentation
3. Open an issue on GitHub

---

**Note**: Remember to update the Lambda function URL in `src/config.js` before deploying! 