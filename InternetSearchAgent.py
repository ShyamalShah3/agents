import boto3
import json
import os
from SearchResults import SearchResults

class InternetSearchAgent:
    _invocation_type = "RequestResponse"
    
    def __init__(self):
        self.lambda_client = boto3.client(
            service_name="lambda",
            region_name=os.environ.get("REGION")
        )

    def search(self, query: str) -> SearchResults:
        try:
            print("Querying Internet Search Plugin")
            response = self.lambda_client.invoke(
                FunctionName=os.environ.get("INTERNET_PLUGIN"),
                InvocationType=self._invocation_type,
                Payload=json.dumps({'query': query})
            )
            print("Parsing Internet Search Plugin Response")
            result = json.loads(response['Payload'].read().decode('utf-8'))
            return SearchResults(result['body']['results'])
        except Exception as e:
            print(f"Error invoking internet plugin: {str(e)}")
            raise
