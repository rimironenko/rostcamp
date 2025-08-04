locals {
  user_data = <<-EOT
              #!/bin/bash
              yum update -y
              yum install -y httpd jq python3 python3-pip
              pip3 install boto3

              # Start and enable Apache
              systemctl start httpd
              systemctl enable httpd

              # Get the instance metadata
              export TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
              export INSTANCE_ID=$(curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id)
              export AVAILABILITY_ZONE=$(curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/placement/availability-zone)
              export REGION=$(curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/placement/region)

              # Create a simple Python script to interact with DynamoDB
              cat <<PYTHON > /var/www/html/dynamodb_test.py
              #!/usr/bin/env python3
              import boto3
              import json
              import uuid
              import os
              from datetime import datetime

              def lambda_handler(event, context):
                  # Create DynamoDB client
                  dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('REGION'))
                  table = dynamodb.Table('example-table')

                  # Create a new item with a UUID as id
                  item_id = str(uuid.uuid4())
                  timestamp = datetime.now().isoformat()

                  # Get environment variables
                  instance_id = os.environ.get('INSTANCE_ID', 'unknown')
                  az = os.environ.get('AVAILABILITY_ZONE', 'unknown')

                  # Put item in DynamoDB
                  response = table.put_item(
                      Item={
                          'id': item_id,
                          'timestamp': timestamp,
                          'message': 'Hello from EC2 instance ' + instance_id,
                          'availability_zone': az
                      }
                  )

                  # Query the table to get all items (for demonstration)
                  scan_response = table.scan()
                  items = scan_response.get('Items', [])

                  return {
                      'statusCode': 200,
                      'inserted_id': item_id,
                      'items': items
                  }

              if __name__ == '__main__':
                  print(json.dumps(lambda_handler(None, None), indent=2, default=str))
              PYTHON

              chmod +x /var/www/html/dynamodb_test.py

              # Export environment variables for the Python script.
              # export INSTANCE_ID="$INSTANCE_ID"
              # export AVAILABILITY_ZONE="$AVAILABILITY_ZONE"

              # Run the script to test DynamoDB and save output
              python3 /var/www/html/dynamodb_test.py > /var/www/html/dynamodb_result.json

              # Create the HTML file with instance and DynamoDB info
              cat <<HTML > /var/www/html/index.html
              <!DOCTYPE html>
              <html>
              <head>
                <title>EC2 Instance with DynamoDB</title>
                <style>
                  body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                  h1, h2 { color: #333; }
                  .info { background-color: #f4f4f4; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
                  pre { background-color: #eee; padding: 10px; border-radius: 5px; overflow-x: auto; }
                </style>
              </head>
              <body>
                <h1>EC2 Instance with DynamoDB Access</h1>
                <div class="info">
                  <p><strong>Hostname:</strong> $(hostname -f)</p>
                  <p><strong>Instance ID:</strong> $INSTANCE_ID</p>
                  <p><strong>Availability Zone:</strong> $AVAILABILITY_ZONE</p>
                </div>

                <h2>DynamoDB Test Results</h2>
                <p>The following shows the result of a test write and read from the DynamoDB table:</p>
                <pre id="dynamodb-result">Loading...</pre>

                <script>
                  fetch('/dynamodb_result.json')
                    .then(response => response.text())
                    .then(data => {
                      document.getElementById('dynamodb-result').textContent = data;
                    })
                    .catch(error => {
                      document.getElementById('dynamodb-result').textContent = 'Error loading DynamoDB results: ' + error;
                    });
                </script>
              </body>
              </html>
              HTML
              EOT
}