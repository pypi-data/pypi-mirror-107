from aws_cdk import (
    core,
    aws_codepipeline as _codepipeline,
    aws_codecommit as _codecommit
)

from rba_cdk import (
  rba_codepipeline_actions
)

from .default_pipeline import DefaultPipeline

class BuildspecPipeline(DefaultPipeline):
  '''
  Bases: rba_cdk.rba_pipelines.DefaultPipeline

  An AWS codepipeline stack that can deploy additional CDK stacks and build according to buildspec.yml file.
  This stack class is opinionated.  It only works with CodeCommit.

  Required parameters: 
  - scope (Construct) 
  - id (str)
  - code_repo_name (str) - name of the CodeCommit Repository.
  - branch_name (str) - name of the branch that pipeline is deploying
  '''  
  def __init__(self, scope: core.Construct, id: str, code_repo: _codecommit.Repository, branch_name: str, **kwargs):
    super().__init__(scope, id, code_repo, branch_name, **kwargs)
    
    build_artifact = _codepipeline.Artifact()

    build_stage = self.add_stage('asBuildspec')
    # create an action to build the docker image
    build_action = rba_codepipeline_actions.DefaultBuildAction(self,
      action_name='CodeBuild',
      input=self.source_artifact,
      outputs=[build_artifact],
      variables_namespace='BuildVariables'
    )
    build_stage.add_actions(build_action)

    self.build_artifact = build_artifact