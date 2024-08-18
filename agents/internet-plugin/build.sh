#!/bin/bash
REPO_NAME='agents-repository'
INTERNET_PLUGIN_IMAGE_TAG='internet-plugin'
REGION='us-west-2'
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Authenticate Docker to ECR
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

# Build the Docker image
docker build . -t $INTERNET_PLUGIN_IMAGE_TAG

# Tag the Docker image
docker tag $INTERNET_PLUGIN_IMAGE_TAG:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:$INTERNET_PLUGIN_IMAGE_TAG

# Push the Docker image to ECR
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:$INTERNET_PLUGIN_IMAGE_TAG

# Output the image URI
echo "Image pushed to ECR: $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:$INTERNET_PLUGIN_IMAGE_TAG"
