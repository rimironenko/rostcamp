locals {
  genai_model_arn = "arn:aws:bedrock:${var.aws_region}::foundation-model/${var.genai_foundational_model_id}"
  bedrock_kb_arn  = "arn:aws:bedrock:${var.aws_region}:${data.aws_caller_identity.current.account_id}:knowledge-base/${var.bedrock_kb_id}"
}