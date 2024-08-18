import os
from aws_cdk import App, Environment
from stacks.ecr_stack import ECRStack
from stacks.agent_stack import AgentStack

app = App()

# Deploy the ECRStack
ecr_stack = ECRStack(app, "ECRStack",
    env=Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region="us-west-2"
    )
)

agent_stack = AgentStack(app, "AgentStack",
    env=Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region="us-west-2"
    )
)

app.synth()
