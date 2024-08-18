from aws_cdk import (
    Stack,
    aws_ecr as ecr,
    aws_iam as iam,
)
from constructs import Construct
from construct.lambda_container_construct import LambdaContainerConstruct
from construct.ecr_construct import EcrConstruct

class AgentStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Get the repository name and image tags from context
        repo_name = self.node.try_get_context("ecr_config")["repository_name"]
        internet_plugin_config = self.node.try_get_context("internet_plugin_lambda")
        chat_agent_config = self.node.try_get_context("chat_agent_lambda")

        # Reference the existing ECR repository by name
        ecr_repository = EcrConstruct.from_repository_name(
            self,
            "AgentsRepository",
            repository_name=repo_name
        )

        # Create the internet-plugin Lambda function
        internet_plugin = LambdaContainerConstruct(
            self,
            "InternetPluginLambda",
            function_name="internet-plugin",
            repository=ecr_repository,
            image_tag=internet_plugin_config["image_tag"],
            environment=internet_plugin_config["environment_variables"],
            memory_size=internet_plugin_config["memory_size"],
            timeout=internet_plugin_config["timeout"]
        )

        # Create the chat-agent Lambda function with proper environment variables
        chat_agent_env_vars = chat_agent_config["environment_variables"]
        chat_agent_env_vars["INTERNET_PLUGIN"] = internet_plugin.function_name

        chat_agent = LambdaContainerConstruct(
            self,
            "ChatAgentLambda",
            function_name="chat-agent",
            repository=ecr_repository,
            image_tag=chat_agent_config["image_tag"],
            environment=chat_agent_env_vars,
            memory_size=chat_agent_config["memory_size"],
            timeout=chat_agent_config["timeout"]
        )

        # Add permissions to ChatAgentLambda to access Bedrock
        chat_agent.add_to_role_policy(iam.PolicyStatement(
            actions=["bedrock:InvokeModel"],
            resources=["*"]
        ))

        # Grant permissions for ChatAgentLambda to invoke the internet-plugin Lambda
        chat_agent.add_to_role_policy(iam.PolicyStatement(
            actions=["lambda:InvokeFunction"],
            resources=[internet_plugin.function_arn]
        ))