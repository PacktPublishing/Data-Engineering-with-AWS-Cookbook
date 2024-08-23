variable "region" { 
  description = "AWS region" 
  type = string 
  default = "us-east-1" 
} 

data "aws_caller_identity" "current" {} 

locals { 
  bucket_name = "terraform-recipe-${data.aws_caller_identity.current.account_id}" 
}

variable "script_file" { 
  type    = string  
  default = "ShellScriptRecipe.py" 
}
