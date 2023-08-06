from aws_cdk import (
    core,
    aws_codebuild as _codebuild,
)

from rba_cdk import (
  rba_ecr,
  rba_codepipeline_actions
)

from .default_pipeline import DefaultPipelineStack

class DockerPipelineStack(DefaultPipelineStack):
  '''
  Bases: rba_cdk.rba_pipelines.DefaultPipelineStack

  An AWS codepipeline stack that can deploy additional CDK stacks and build Docker images according to buildspec.yml file.
  This stack class is opinionated.  It only works with CodeCommit.

  Required parameters: 
  - scope (Construct) 
  - id (str)
  - code_repo_name (str) - name of the CodeCommit Repository.
  - branch_name (str) - name of the branch that pipeline is deploying
  - ecr_tld (str) - FQDN of AWS Elastic Container Registry. example: 765750088304.dkr.ecr.us-west-2.amazonaws.com
  '''  
  def __init__(self, scope: core.Construct, id: str, code_repo_name: str, branch_name: str, ecr_tld: str, **kwargs):
    super().__init__(scope, id, code_repo_name, branch_name, **kwargs)

    # create ecr repository for docker images if on master branch
    if branch_name == 'master':
      ecr_repo = rba_ecr.ECR(self, code_repo_name)
    
    docker_build_stage = self.pipeline.add_stage('DockerBuild')
    # create an action to build the docker image
    docker_build_action = rba_codepipeline_actions.DockerBuildAction(self,
      action_name='DockerBuild',
      input=self.source_artifact,
      variables_namespace='BuildVariables',
      environment_variables={
        "ECR_REPO_URI": _codebuild.BuildEnvironmentVariable(value=f'{ecr_tld}/{code_repo_name}')
      } 
    )
    docker_build_stage.add_actions(docker_build_action)
