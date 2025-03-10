# Output the public IP of the EC2 instance
output "public_ip" {
  value = aws_instance.web.public_ip
}

# Output the DynamoDB table name
output "dynamodb_table_name" {
  value = aws_dynamodb_table.example_table.name
}

# Output the AMI ID used
output "ami_id" {
  value = data.aws_ami.amazon_linux_2.id
}

# Output the AMI name
output "ami_name" {
  value = data.aws_ami.amazon_linux_2.name
}