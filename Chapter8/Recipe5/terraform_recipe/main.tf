provider "aws" {
  region = var.region
}

resource "aws_s3_bucket" "bucket" {
  bucket = local.bucket_name
}

resource "aws_s3_object" "script" {
  bucket = local.bucket_name
  key    = "scripts/${var.script_file}"
  source = var.script_file
  depends_on = [
    aws_s3_bucket.bucket
  ]
}
resource "aws_iam_role" "glue" {
  name = "AWSGlueServiceRoleTerraformRecipe"
  managed_policy_arns = [ 
"arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess",
"arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
  ]
  assume_role_policy = jsonencode(
        {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Action": "sts:AssumeRole",
              "Principal": {
                "Service": "glue.amazonaws.com"
              },
              "Effect": "Allow",
              "Sid": ""
            }
          ]
        }
    )
}

resource "aws_glue_job" "shell_job" {
  name     = "TerraformRecipeShellJob"
  role_arn = aws_iam_role.glue.arn
 
  command {
    name = "pythonshell"
    python_version = "3.9"
    script_location = "s3://${local.bucket_name}/scripts/${var.script_file}"
  }
} 
