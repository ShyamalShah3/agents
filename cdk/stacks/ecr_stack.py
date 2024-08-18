from aws_cdk import (
    Stack,
    aws_ecr as ecr,
    RemovalPolicy,
)
from constructs import Construct
from construct.ecr_construct import EcrConstruct

class ECRStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Get configuration from cdk.json
        config = self.node.try_get_context("ecr_config")
        repo_name = config["repository_name"]

        # Create an ECR repository
        self.ecr_construct = EcrConstruct(
            self,
            "AgentsRepository",
            repository_name = repo_name,
            image_scan_on_push = True
        )