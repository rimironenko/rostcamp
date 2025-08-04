# Output EC2 and S3 information
output "ec2_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.web.public_ip
}

output "s3_bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.demo_bucket.id
}

output "web_url" {
  description = "URL to access the demo web application"
  value       = "http://${aws_instance.web.public_ip}"
}