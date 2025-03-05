import os
from github_deployments import GithubDeployment

gh = GithubDeployment()

# gh.delete_deployment()
gh.update_deployment()
