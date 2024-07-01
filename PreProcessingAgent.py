from typing import Optional
from BedrockClient import BedrockClient
from FoundationalModel import FoundationalModel
from PreProcessingAgentResponse import PreProcessingAgentResponse
from XMLParser import XMLParser

class PreProcessingAgent:
    def __init__(self, bedrock_client: BedrockClient):
        self.bedrock_client = bedrock_client
        self.xml_parser = XMLParser()

    def process(self, query: str, model: FoundationalModel) -> PreProcessingAgentResponse:

        prompt = f"""
        You are a pre-processing agent whose job is to determine if an internet search is required to answer the user's question. If yes, then you
        will provide the input parameters to the search query using search engine optimization as best as possible making sure to use clear & concise
        questions to get relevant information from the internet to answer the question.

        Here is what the input parameters to the internet search look like:
        <search_query></search_query>
        where the <search_query> is what you are searching on the internet.

        Here are what your example responses look like:

        Example Response 1:
        <response>
            <use_internet>True</use_internet>
            <search_query>Test Question to search Internet</search_query>
        </response>

        Example Response 2:
        <response>
            <use_internet>False</use_internet>
        </response>

        Make sure to answer using only xml.

        Here is the user's prompt:

        <prompt>{query}</prompt>

        Should we use the internet to help answer this question?
        """
        print("Querying Pre Processing Agent")
        response = self.bedrock_client.query_model(model, prompt)
        print("Parsing Pre Processing Agent Response", response)
        return self.xml_parser.parse_preprocessing_agent_response(response)
