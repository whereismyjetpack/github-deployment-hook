## GitHub Deployment Hook
A docker container that is intended to be used as an ArgoCD sync hook, that updates a Github Deployment on sync

## Usage
First we create a PreSync Hook that sets the deployment to in_progress
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: github-deployment-start
  annotations:
    argocd.argoproj.io/hook: PreSync
    spec:
      template:
        spec:
          containers:
          - name: github-deployment-hook
            image: your-docker-image:latest
            env:
            - name: ENVIRONMENT_NAME
              value: "development"
            - name: GITHUB_REPO
              value: "whereismyjetpack/github-deployment-hook"
            - name: GITHUB_REF
              value: "c5ed9b6b80c0e14341d1241520306252c5a50b11"
            - name: GITHUB_TOKEN
              valueFrom:
                secretKeyRef:
                  name: github-token-secret
                  key: token
            - name: DEPLOYMENT_STATE
              value: "in_progress"
          restartPolicy: Never
```

Then we set a PostSync hook to set the deployment as successful
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: github-deployment-end
  annotations:
    argocd.argoproj.io/hook: PostSync
spec:
  template:
    spec:
      containers:
      - name: github-deployment-hook
        image: your-docker-image:latest
        env:
        - name: ENVIRONMENT_NAME
          value: "development"
        - name: GITHUB_REPO
          value: "whereismyjetpack/github-deployment-hook"
        - name: GITHUB_REF
          value: "c5ed9b6b80c0e14341d1241520306252c5a50b11"
        - name: GITHUB_TOKEN
          valueFrom:
            secretKeyRef:
              name: github-token-secret
              key: token
        - name: DEPLOYMENT_STATE
          value: "success"
      restartPolicy: Never
```
Finally, we set a SyncFail hook to set the deployment state to error
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: github-deployment-fail
  annotations:
    argocd.argoproj.io/hook: SyncFail
spec:
  template:
    spec:
      containers:
      - name: github-deployment-hook
        image: your-docker-image:latest
        env:
        - name: ENVIRONMENT_NAME
          value: "development"
        - name: GITHUB_REPO
          value: "whereismyjetpack/github-deployment-hook"
        - name: GITHUB_REF
          value: "c5ed9b6b80c0e14341d1241520306252c5a50b11"
        - name: GITHUB_TOKEN
          valueFrom:
            secretKeyRef:
              name: github-token-secret
              key: token
        - name: DEPLOYMENT_STATE
          value: "error"
      restartPolicy: Never
```

## Environment Variables

| Variable         | Description                                                                 | Default                        |
|------------------|-----------------------------------------------------------------------------|--------------------------------|
| ENVIRONMENT_NAME | The name of the environment (e.g., "development").                          |                                |
| GITHUB_REPO      | The GitHub repository in the format "owner/repo"                            |                                |
|                  | (e.g., "whereismyjetpack/github-deployment-hook").                          |                                |
| GITHUB_REF       | The GitHub reference (e.g., commit SHA).                                    |                                |
| GITHUB_TOKEN     | The GitHub token used for authentication, sourced from a Kubernetes secret. |                                |
| GITHUB_API_URL   | The GitHub API URL (optional, defaults to "https://api.github.com").        | "https://api.github.com"       |
| DEPLOYMENT_STATE | The state of the deployment (e.g., "error", "failure", "inactive"           |                                |
|                  | , "in_progress", "queued", "pending", "success"). |                         |                                |