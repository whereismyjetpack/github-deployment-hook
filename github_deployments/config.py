from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
import re


class Config(BaseSettings):
    model_config = SettingsConfigDict()
    github_token: str
    github_repo: str
    environment_name: str
    github_ref: str
    github_api_url: str = "https://api.github.com"
    deployment_state: str

    @field_validator("github_repo")
    def validate_github_repo(cls, value):
        if not re.match(r".*/.*", value):
            raise ValueError("github_repo must match the pattern owner/repo")
        return value

    @field_validator("deployment_state")
    def validate_deployment_state(cls, value):
        valid_states = [
            "error",
            "in_progress",
            "success",
            "failure",
            "inactive",
            "queued",
            "pending",
        ]
        if value not in valid_states:
            raise ValueError(f"deployment_state must be one of {valid_states}")
        return value
