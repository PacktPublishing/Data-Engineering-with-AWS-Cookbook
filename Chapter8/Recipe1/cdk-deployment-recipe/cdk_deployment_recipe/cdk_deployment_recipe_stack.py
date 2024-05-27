from aws_cdk import (
  Stack,
  Stage,
  aws_codecommit as codecommit,
  aws_glue as glue,
  aws_iam as iam,
  aws_s3 as s3,
  aws_s3_deployment as s3_deploy
)
from aws_cdk.pipelines import (
  CodePipeline,
  CodePipelineSource,
  ShellStep
)
from constructs import Construct
class CdkDeploymentRecipeStack(Stack):
  def __init__(self, scope: Construct, 
               construct_id: str, **kwargs):
    super().__init__(scope, construct_id, **kwargs)

    repo = codecommit.Repository.from_repository_name(self,
            "DeployRecipeRepo", repository_name="cdk-deployment-recipe")
    git_source = CodePipelineSource.code_commit(repo, "master")
    pipeline = CodePipeline(self, "Pipeline",
       pipeline_name="RecipePipeline",
         synth=ShellStep("Synth",
                input=git_source,
                commands=[
                 "npm install -g aws-cdk",
         "python -m pip install -r requirements.txt",
                 "cdk synth"]
                )
        )
    pipeline.add_stage(GlueStage(self, "prod"))

class GlueStage(Stage):
  def __init__(self, scope: Construct,  
               construct_id: str, **kwargs):
    super().__init__(scope, construct_id, **kwargs)
    GlueAppStack(self, "GlueAppStack",
                 stage=self.stage_name)
class GlueAppStack(Stack):
  def __init__(self, scope: Construct, 
            construct_id: str, stage: str, **kwargs):
    super().__init__(scope, construct_id, **kwargs)
    bucket_name = f"deployment-recipe-{self.account}-{stage}"
    bucket = s3.Bucket(self, id="GlueBucket", 
                    bucket_name=bucket_name)
    deployment = s3_deploy.BucketDeployment(self,
       "DeployCode", destination_bucket=bucket, 
       sources=[s3_deploy.Source.asset("./glue")])
    role_name = f"AWSGlueServiceRole-CdkRecipe-{stage}"
    job_role = iam.Role(self, id=role_name,
              role_name=role_name, managed_policies=[
      iam.ManagedPolicy.from_managed_policy_arn(self, 
      "glue-service", "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole")
                  ],
                  assumed_by=iam.ServicePrincipal( 
                             "glue.amazonaws.com")
               )
    job_role.add_to_policy(iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                resources=[
                    f'arn:aws:s3:::{bucket_name}',
                    f'arn:aws:s3:::{bucket_name}/*'
                ],
                actions=[
                    's3:ListBucket',
                    's3:GetObject',
                    's3:PutObject'
                ]
               )
             )
    job = glue.CfnJob(
            self,
            "glue_CDK_job",
            command = glue.CfnJob.JobCommandProperty(
                    name = "pythonshell",
                    python_version= '3.9',
                    script_location = f's3://{bucket_name}/GlueShellScript.py'
                ),
                role= job_role.role_arn,
                name= "deployment_recipe_glueshell",
                glue_version="3.0"
) 
