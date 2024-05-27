resource "aws_glue_job" "tfer--recipe-shell-reveng" {
  command {
    name            = "pythonshell"
    python_version  = "3.9"
    script_location = "s3://somebucket/yourscript.py"
  }

  execution_property {
    max_concurrent_runs = "1"
  }

  glue_version      = "4.0"
  max_capacity      = "0.0625"
  max_retries       = "1"
  name              = "recipe-shell-reveng"
  role_arn          = "arn:aws:iam::123456789:role/SomeRoleForGlue"
  timeout           = "2880"
}
