from aws_cdk import (
    core,
    aws_codepipeline as _codepipeline,
    aws_codepipeline_actions as _codepipeline_actions,
    aws_codecommit as _codecommit,
    aws_codebuild as _codebuild,
    pipelines as _pipelines
)


class DefaultPipeline(_pipelines.CdkPipeline):
  '''
  Bases aws_cdk.pipelines

  An AWS codepipeline stack that can deploy additional CDK stacks.
  This stack class is opinionated.  It only works with CodeCommit.

  Required parameters: 
  - scope (Construct) 
  - id (str)
  - code_repo_name (str) - name of the CodeCommit Repository.
  - branch_name (str) - name of the branch that pipeline is deploying
  '''  
  def __init__(self, scope: core.Construct, id: str, code_repo: _codecommit.Repository, branch_name: str, **kwargs):
    source_artifact = _codepipeline.Artifact()
    cloud_assembly_artifact = _codepipeline.Artifact()

    source_action=_codepipeline_actions.CodeCommitSourceAction(
      action_name='CodeCommit',
      output=source_artifact,
      repository=code_repo,
      branch=branch_name,
      variables_namespace='SourceVariables',
      code_build_clone_output=True
    )

    synth_action=_pipelines.SimpleSynthAction(
      source_artifact=source_artifact,
      cloud_assembly_artifact=cloud_assembly_artifact,
      install_commands=['npm install -g aws-cdk && npm install esbuild && pip install -r requirements.txt'],
      environment_variables={
        'COMMIT_ID': _codebuild.BuildEnvironmentVariable(value='#{SourceVariables.CommitId}'),
        'BRANCH_NAME': _codebuild.BuildEnvironmentVariable(value='#{SourceVariables.BranchName}')
      },
      synth_command='cdk synth --quiet')

    super().__init__(scope, id, 
      cloud_assembly_artifact=cloud_assembly_artifact,
      pipeline_name=id,
      source_action=source_action,
      synth_action=synth_action,
      **kwargs
    )

    self.source_artifact=source_artifact


