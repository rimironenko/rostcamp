#!/bin/bash

# ChatGPT Lambda Website - S3 Deployment Script
# This script builds the React app and uploads it to an S3 bucket

set -e  # Exit on any error

# Configuration
BUCKET_NAME="your-chatgpt-lambda-website-bucket"
REGION="us-east-1"
BUILD_DIR="build"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 ChatGPT Lambda Website - S3 Deployment${NC}"
echo "================================================"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI is not installed. Please install it first.${NC}"
    echo "Visit: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
    exit 1
fi

# Check if user is authenticated with AWS
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}❌ AWS CLI is not configured. Please run 'aws configure' first.${NC}"
    exit 1
fi

# Check if bucket name is configured
if [ "$BUCKET_NAME" = "your-chatgpt-lambda-website-bucket" ]; then
    echo -e "${YELLOW}⚠️  Please update the BUCKET_NAME variable in this script before running.${NC}"
    exit 1
fi

echo -e "${BLUE}📦 Building React application...${NC}"
npm run build

if [ ! -d "$BUILD_DIR" ]; then
    echo -e "${RED}❌ Build directory not found. Build may have failed.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Build completed successfully!${NC}"

# Check if bucket exists
echo -e "${BLUE}🔍 Checking if S3 bucket exists...${NC}"
if aws s3 ls "s3://$BUCKET_NAME" 2>&1 | grep -q 'NoSuchBucket'; then
    echo -e "${YELLOW}⚠️  Bucket '$BUCKET_NAME' does not exist. Creating it...${NC}"
    aws s3 mb "s3://$BUCKET_NAME" --region "$REGION"
    
    # Configure bucket for static website hosting
    echo -e "${BLUE}🌐 Configuring bucket for static website hosting...${NC}"
    aws s3 website "s3://$BUCKET_NAME" --index-document index.html --error-document index.html
    
    # Set bucket policy for public read access
    echo -e "${BLUE}🔓 Setting bucket policy for public read access...${NC}"
    cat > bucket-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::$BUCKET_NAME/*"
        }
    ]
}
EOF
    
    aws s3api put-bucket-policy --bucket "$BUCKET_NAME" --policy file://bucket-policy.json
    rm bucket-policy.json
    
    echo -e "${GREEN}✅ Bucket created and configured successfully!${NC}"
else
    echo -e "${GREEN}✅ Bucket '$BUCKET_NAME' already exists.${NC}"
fi

# Upload files to S3
echo -e "${BLUE}📤 Uploading files to S3...${NC}"
aws s3 sync "$BUILD_DIR" "s3://$BUCKET_NAME" --delete

echo -e "${GREEN}✅ Files uploaded successfully!${NC}"

# Get the website URL
WEBSITE_URL=$(aws s3api get-bucket-website --bucket "$BUCKET_NAME" --query 'WebsiteEndpoint' --output text 2>/dev/null || echo "")

if [ -n "$WEBSITE_URL" ]; then
    echo ""
    echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
    echo -e "${BLUE}🌐 Your website is available at:${NC}"
    echo -e "${GREEN}   http://$WEBSITE_URL${NC}"
    echo ""
    echo -e "${YELLOW}⚠️  Important:${NC}"
    echo -e "${YELLOW}   - Update the Lambda function URL in src/config.js${NC}"
    echo -e "${YELLOW}   - Ensure your Lambda function has CORS enabled${NC}"
    echo -e "${YELLOW}   - Test the authentication with the default credentials${NC}"
else
    echo -e "${YELLOW}⚠️  Could not retrieve website URL. Please check your bucket configuration.${NC}"
fi

echo ""
echo -e "${BLUE}📋 Next steps:${NC}"
echo "1. Update Lambda function URL in src/config.js"
echo "2. Test the website functionality"
echo "3. Update authentication credentials if needed"
echo "4. Configure your Lambda function with proper CORS headers" 