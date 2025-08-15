
module "website_bucket" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "4.2.2"

  bucket        = "2025-08-pm-${random_pet.this.id}"
  force_destroy = true
  website = {
    index_document = "index.html"
    error_document = "index.html"
  }
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
  attach_policy           = true
  policy                  = data.aws_iam_policy_document.bucket_policy.json


  tags = var.aws_resource_tags

}

####################################################
# Lambda Function (building from source)
####################################################

module "lambda_function" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "7.14.0"

  function_name              = "bedrock-rag-lambda-function-${random_pet.this.id}"
  description                = "AWS Lambda function to invoke Amazon Bedrock model"
  handler                    = "index.handler"
  runtime                    = "python3.13"
  publish                    = true
  timeout                    = 60
  create_lambda_function_url = true
  cors = {
    allow_origins = ["http://${module.website_bucket.s3_bucket_website_endpoint}"]
    allow_methods = ["*"]
    allow_headers = ["Content-Type"]
  }

  source_path = "${path.module}/src"

  environment_variables = {
    BEDROCK_KB_ID : var.bedrock_kb_id,
    GEN_AI_MODEL_ARN : local.genai_model_arn
  }

  attach_policies = true
  policies        = ["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"]

  attach_policy_statements = true
  policy_statements = {
    invoke_bedrock_model = {
      effect = "Allow",
      actions = [
        "bedrock:InvokeModel"
      ],
      resources = [
        local.genai_model_arn
      ]
    },
    retrieve_and_generate = {
      effect = "Allow",
      actions = [
        "bedrock:RetrieveAndGenerate",
        "bedrock:Retrieve",
      ],
      resources = [
        local.bedrock_kb_arn
      ]
    }
  }

  tags = var.aws_resource_tags

}

resource "random_pet" "this" {
  length = 2
}