from aws_cdk import (
    aws_ecr as ecr,
    RemovalPolicy,
)
from constructs import Construct
from typing import Optional

class EcrConstruct(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        repository_name: str,
        removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
        image_scan_on_push: bool = True,
        lifecycle_rules: Optional[list[ecr.LifecycleRule]] = None
    ):
        super().__init__(scope, id)

        self.repository_name = repository_name
        self.repository = ecr.Repository(
            self,
            repository_name,
            repository_name=repository_name,
            removal_policy=removal_policy,
            image_scan_on_push=image_scan_on_push,
            lifecycle_rules=lifecycle_rules or []
        )

    @property
    def repository_arn(self) -> str:
        return self.repository.repository_arn

    @property
    def repository_uri(self) -> str:
        return self.repository.repository_uri

    @staticmethod
    def from_repository_name(
        scope: Construct,
        id: str,
        repository_name: str
    ) -> ecr.IRepository:
        """Reference an existing ECR repository by name."""
        return ecr.Repository.from_repository_name(
            scope,
            id,
            repository_name
        )