from aws_cdk import (
  core,
  aws_iam as _iam,
  aws_codebuild as _codebuild,
  aws_codepipeline_actions as _codepipeline_actions
)

class DefaultBuildAction(_codepipeline_actions.CodeBuildAction):
    '''
    Bases: aws_cdk.aws_codepipeline_actions.CodeBuildAction
    https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_codepipeline_actions/CodeBuildAction.html

    It creates a generic CodeBuild project that does build according to buildspec.yml

    Required parameters: 
    - scope (Construct) 
    - input (Artifact)
    - output (List[Artifact])
    '''
    def __init__(self, scope: core.Construct, **kwargs):
      if 'project' not in kwargs:
        # create codebuild project
        default_project = _codebuild.PipelineProject(scope, 'DefaultCodeBuild',
          environment=_codebuild.BuildEnvironment(build_image=_codebuild.LinuxBuildImage.STANDARD_5_0)
        )
        kwargs['project'] = default_project
      super().__init__(**kwargs)



class DockerBuildAction(_codepipeline_actions.CodeBuildAction):
    '''
    Bases: aws_cdk.aws_codepipeline_actions.CodeBuildAction
    https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_codepipeline_actions/CodeBuildAction.html

    It creates a generic CodeBuild project that builds Docker images according to buildspec.yml

    Required parameters: 
    - scope (Construct) 
    - input (Artifact)
    '''
    def __init__(self, scope: core.Construct, **kwargs):
      if 'project' not in kwargs:
        # create codebuild project
        default_project = _codebuild.PipelineProject(scope, 'DockerCodeBuild', 
          environment=_codebuild.BuildEnvironment(
            privileged=True,
            build_image=_codebuild.LinuxBuildImage.STANDARD_5_0
          )
        )
        # add policy statement that grants ECR access to the codebuild project Role
        ecr_policy = _iam.PolicyStatement(
          actions=['ecr:*'],
          resources=['*']
        )
        default_project.add_to_role_policy(ecr_policy)

        kwargs['project'] = default_project
      super().__init__(**kwargs)

