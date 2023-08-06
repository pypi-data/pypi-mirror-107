import os
import pygit2


def get_branch_name():
  '''
  this function returns the branch name as str.
  '''
  if 'BRANCH_NAME' in os.environ:
    return os.environ['BRANCH_NAME']
  else:
    try:
      return pygit2.Repository('.').head.shorthand
    except Exception as e:
      print(e)
      print('not a git repo, cannot determine branch')

