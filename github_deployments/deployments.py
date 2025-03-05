from .config import Config
import requests
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class GithubDeployment:
    def __init__(self):
        self.config = Config()
        self.headers = {
            "Authorization": f"token {self.config.github_token}",
            "accept": "application/vnd.github.ant-man-preview+json",
        }

    def delete_deployment(self):
        deployment_id = self.get_deployment_from_ref()
        if not deployment_id:
            return
        resp = requests.delete(
            f"{self.config.github_api_url}/repos/{self.config.github_repo}/deployments/{deployment_id}",
            headers=self.headers,
        )
        if resp.status_code != 204:
            logging.error(f"Failed to delete deployment: {resp.json()}")
            raise Exception(f"Failed to delete deployment: {resp.json()}")

        return {"status": "success"}

    def get_deployment_from_ref(self):
        ref = self.config.github_ref
        resp = requests.get(
            f"{self.config.github_api_url}/repos/{self.config.github_repo}/deployments",
            headers=self.headers,
        )
        if resp.status_code != 200:
            logging.error(f"Failed to get deployments: {resp.json()}")
            raise Exception(f"Failed to get deployments: {resp.json()}")

        deployments = resp.json()
        for deployment in deployments:
            if deployment["ref"] == ref:
                logging.info(f"Found deployment: {deployment['id']}")
                return deployment["id"]

        return None

    def update_deployment(self):
        deployment_id = self.get_deployment_from_ref()
        if not deployment_id:
            logging.info("Existing Deployment not found. Creating a new deployment.")
            deployment_id = self.create_deployment()

        data = {
            "state": self.config.deployment_state,
        }

        resp = requests.post(
            f"{self.config.github_api_url}/repos/{self.config.github_repo}/deployments/{deployment_id}/statuses",
            headers=self.headers,
            json=data,
        )

        if resp.status_code != 201:
            logging.error(f"Failed to update deployment: {resp.json()}")
            raise Exception(f"Failed to update deployment: {resp.json()}")

        logging.info(f"Deployment updated")

    def create_deployment(self):
        config = Config()
        headers = {
            "Authorization": f"token {config.github_token}",
            "accept": "application/vnd.github.ant-man-preview+json",
        }

        data = {
            "ref": config.github_ref,
            "environment": config.environment_name,
            "auto_merge": False,
        }

        resp = requests.post(
            f"{config.github_api_url}/repos/{config.github_repo}/deployments",
            headers=headers,
            json=data,
        )

        if resp.status_code != 201:
            logging.error(f"Failed to create deployment: {resp.json()}")
            raise Exception(
                f"Failed to create deployment: {
                resp.json()
            }"
            )

        logging.info(f"Deployment created")

        return resp.json()["id"]
