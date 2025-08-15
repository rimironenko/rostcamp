data "aws_region" "current" {}
data "aws_caller_identity" "current" {}
data "aws_iam_policy_document" "bucket_policy" {
  statement {
    principals {
      type        = "*"
      identifiers = ["*"]
    }

    actions = [
      "s3:GetObject",
    ]

    resources = [
      "${module.website_bucket.s3_bucket_arn}/*",
    ]
  }
}