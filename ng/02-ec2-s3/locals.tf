locals {
  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y httpd
              yum install -y aws-cli
              systemctl start httpd
              systemctl enable httpd
              amazon-linux-extras enable php7.4
              yum clean metadata
              yum install -y php php-cli

              # Create a simple web page to demonstrate S3 connectivity
              cat > /var/www/html/index.html << 'HTMLCONTENT'
              <!DOCTYPE html>
              <html>
              <head>
                <title>EC2 to S3 Connectivity Demo</title>
                <style>
                  body { font-family: Arial, sans-serif; margin: 40px; }
                  h1 { color: #333; }
                  .container { max-width: 800px; margin: 0 auto; }
                  .result { padding: 10px; border: 1px solid #ddd; margin-top: 10px; }
                  button { padding: 8px 16px; background-color: #4CAF50; color: white; border: none; cursor: pointer; margin-right: 10px; }
                  input { padding: 8px; width: 300px; }
                </style>
              </head>
              <body>
                <div class="container">
                  <h1>EC2 to S3 Connectivity Demo</h1>
                  <p>This page demonstrates CRUD operations between this EC2 instance and the S3 bucket.</p>

                  <h2>Create/Upload File</h2>
                  <input type="text" id="createContent" placeholder="Enter content to save">
                  <button onclick="createFile()">Upload to S3</button>
                  <div id="createResult" class="result"></div>

                  <h2>Read/List Files</h2>
                  <button onclick="listFiles()">List S3 Files</button>
                  <div id="listResult" class="result"></div>

                  <h2>Read File Contents</h2>
                  <input type="text" id="readFilename" placeholder="Enter filename to read">
                  <button onclick="readFile()">Get from S3</button>
                  <div id="readResult" class="result"></div>

                  <h2>Delete File</h2>
                  <input type="text" id="deleteFilename" placeholder="Enter filename to delete">
                  <button onclick="deleteFile()">Delete from S3</button>
                  <div id="deleteResult" class="result"></div>
                </div>

                <script>
                  const bucketName = "${aws_s3_bucket.demo_bucket.id}";

                  async function createFile() {
                    const content = document.getElementById('createContent').value;
                    const filename = "file-" + new Date().getTime() + ".txt";
                    const result = document.getElementById('createResult');

                    result.innerHTML = "Creating file...";

                    try {
                      const response = await fetch('/create.php', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                        body: `filename=$${encodeURIComponent(filename)}&content=$${encodeURIComponent(content)}`
                      });

                      const data = await response.text();
                      result.innerHTML = data;
                    } catch (error) {
                      result.innerHTML = "Error: " + error;
                    }
                  }

                  async function listFiles() {
                    const result = document.getElementById('listResult');
                    result.innerHTML = "Listing files...";

                    try {
                      const response = await fetch('/list.php');
                      const data = await response.text();
                      result.innerHTML = data;
                    } catch (error) {
                      result.innerHTML = "Error: " + error;
                    }
                  }

                  async function readFile() {
                    const filename = document.getElementById('readFilename').value;
                    const result = document.getElementById('readResult');

                    if (!filename) {
                      result.innerHTML = "Please enter a filename";
                      return;
                    }

                    result.innerHTML = "Reading file...";

                    try {
                      const response = await fetch('/read.php?filename=' + encodeURIComponent(filename));
                      const data = await response.text();
                      result.innerHTML = data;
                    } catch (error) {
                      result.innerHTML = "Error: " + error;
                    }
                  }

                  async function deleteFile() {
                    const filename = document.getElementById('deleteFilename').value;
                    const result = document.getElementById('deleteResult');

                    if (!filename) {
                      result.innerHTML = "Please enter a filename";
                      return;
                    }

                    result.innerHTML = "Deleting file...";

                    try {
                      const response = await fetch('/delete.php?filename=' + encodeURIComponent(filename));
                      const data = await response.text();
                      result.innerHTML = data;
                    } catch (error) {
                      result.innerHTML = "Error: " + error;
                    }
                  }
                </script>
              </body>
              </html>
              HTMLCONTENT

              # Create PHP scripts to handle S3 operations
              cat > /var/www/html/create.php << 'PHPCONTENT'
              <?php
              $bucket = '${aws_s3_bucket.demo_bucket.id}';

              if ($_SERVER['REQUEST_METHOD'] === 'POST') {
                  $filename = $_POST['filename'] ?? '';
                  $content = $_POST['content'] ?? '';

                  if (empty($filename) || empty($content)) {
                      echo "Error: Filename and content are required";
                      exit;
                  }

                  // Create a temporary file for the content
                  $temp_file = tempnam(sys_get_temp_dir(), 's3upload');
                  file_put_contents($temp_file, $content);

                  // Use the temporary file for the upload
                  $command = "aws s3api put-object --bucket $bucket --key $filename --body $temp_file 2>&1";
                  $output = shell_exec($command);

                  // Clean up the temporary file
                  unlink($temp_file);

                  echo json_encode([
                      'success' => !empty($output),
                      'message' => !empty($output) ? "File created successfully: $filename" : "Error creating file",
                      'details' => $output
                  ]);
              }
              ?>
              PHPCONTENT

              cat > /var/www/html/list.php << 'PHPCONTENT'
              <?php
              $bucket = '${aws_s3_bucket.demo_bucket.id}';

              $command = "aws s3 ls s3://$bucket 2>&1";
              $output = shell_exec($command);

              if ($output) {
                  echo "<pre>$output</pre>";
              } else {
                  echo "No files found or error occurred";
              }
              ?>
              PHPCONTENT

              cat > /var/www/html/read.php << 'PHPCONTENT'
              <?php
              $bucket = '${aws_s3_bucket.demo_bucket.id}';

              $filename = $_GET['filename'] ?? '';

              if (empty($filename)) {
                  echo "Error: Filename is required";
                  exit;
              }

              $command = "aws s3 cp s3://$bucket/$filename - 2>&1";
              $output = shell_exec($command);

              if ($output) {
                  echo "<pre>$output</pre>";
              } else {
                  echo "Error reading file";
              }
              ?>
              PHPCONTENT

              cat > /var/www/html/delete.php << 'PHPCONTENT'
              <?php
              $bucket = '${aws_s3_bucket.demo_bucket.id}';

              $filename = $_GET['filename'] ?? '';

              if (empty($filename)) {
                  echo "Error: Filename is required";
                  exit;
              }

              $command = "aws s3 rm s3://$bucket/$filename 2>&1";
              $output = shell_exec($command);

              if ($output) {
                  echo "File deleted successfully";
              } else {
                  echo "Error deleting file: $output";
              }
              ?>
              PHPCONTENT

              # Install PHP for the web interface
              yum install -y php

              # Restart Apache to apply changes
              systemctl restart httpd
              EOF
}