variable "aws_region" {
  description = "AWS Region to deploy the infrastructure"
  type        = string
  default     = "us-east-1"
}

variable "genai_foundational_model_id" {
  description = "Bedrock Foundational model to use for RAG"
  type        = string
  default     = "anthropic.claude-3-5-sonnet-20240620-v1:0"
}

variable "aws_resource_tags" {
  description = "A map of tags to add to AWS resources"
  type        = map(string)
  default = {
    Application = "demo-2025-08-pm"
  }
}

variable "bedrock_kb_id" {
  description = "Existing Bedrock KB ID"
  type        = string
  default     = "7IFSI7JWE3"
}