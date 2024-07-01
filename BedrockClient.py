import json
import os
import boto3
from FoundationalModel import FoundationalModel
from typing import Dict,Any

class BedrockClient:
    anthropic_models = {FoundationalModel.CLAUDE_3_SONNET, FoundationalModel.CLAUDE_3_HAIKU}
    llama_models = {FoundationalModel.LLAMA_3_70B, FoundationalModel.LLAMA_3_8B}
    
    accept = 'application/json'
    content_type = 'application/json'

    def __init__(self):
        self._region = os.environ.get("REGION")
        self._runtime_client = boto3.client(
            service_name="bedrock-runtime",
            region_name=self._region
        )

    def _get_query_request_body(self, model: FoundationalModel, prompt: str) -> Dict[str, Any]:
        if model in self.anthropic_models:
            return {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": model.model_max_tokens,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": model.model_temperature
            }
        elif model in self.llama_models:
            return {
                "prompt": prompt,
                "temperature": model.model_temperature,
                "max_gen_len": model.model_max_tokens
            }
        raise ValueError(f"{model.model_name} is not currently supported")

    def _parse_query_response_body(self, model: FoundationalModel, response_body: Dict[str, Any]) -> str:
        if model in self.anthropic_models:
            return response_body.get('content')[0].get('text')
        elif model in self.llama_models:
            return response_body.get('generation')
        raise ValueError(f"{model.model_name} is not currently supported")

    def query_model(self, model: FoundationalModel, prompt: str) -> str:
        request_body = json.dumps(self._get_query_request_body(model, prompt))
        try:
            response = self._runtime_client.invoke_model(
                body=request_body,
                modelId=model.model_id,
                accept=self.accept,
                contentType=self.content_type
            )
            response_body = json.loads(response.get('body').read())
            return self._parse_query_response_body(model, response_body)
        except Exception as e:
            print(f"Error querying model: {str(e)}")
            raise
