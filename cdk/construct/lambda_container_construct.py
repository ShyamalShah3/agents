from aws_cdk import (
    aws_lambda as lambda_,
    aws_ecr as ecr,
    aws_iam as iam,
    Duration
)
from constructs import Construct
from typing import Dict, Optional

class LambdaContainerConstruct(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        function_name: str,
        repository: ecr.IRepository,
        image_tag: str,
        environment: Optional[Dict[str, str]] = None,
        memory_size: int = 128,
        timeout: int = 900
    ):
        super().__init__(scope, id)

        self.function = lambda_.DockerImageFunction(
            self,
            f"{function_name}LambdaFunction",
            function_name=function_name,
            code=lambda_.DockerImageCode.from_ecr(
                repository=repository,
                tag_or_digest=image_tag
            ),
            memory_size=memory_size,
            timeout=Duration.seconds(timeout),
            environment=environment or {},
            architecture=lambda_.Architecture.ARM_64
        )

    def add_to_role_policy(self, policy_statement: iam.PolicyStatement) -> None:
        self.function.add_to_role_policy(policy_statement)

    @property
    def function_name(self) -> str:
        return self.function.function_name

    @property
    def function_arn(self) -> str:
        return self.function.function_arn