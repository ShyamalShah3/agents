import json
from BedrockClient import BedrockClient
from FoundationalModel import FoundationalModel
from XMLParser import XMLParser
from SearchResults import SearchResults


class ResponseAgent:
    def __init__(self, bedrock_client: BedrockClient):
        self.bedrock_client = bedrock_client
        self.xml_parser = XMLParser()

    def generate_response(self, query: str, model: FoundationalModel, search_results: SearchResults) -> str:

        prompt = f"""
        You are a question answering agent. You may be provided internet search results to help aid in answering the question. If internet search results
        are provided to you, prioritize using the search results in your answers. If the search results are not helpful in answering the question, make
        sure to mention that in your response.

        The internet search results will be provided to you in the following format:
        <search_results>
            <result>
                <title></title>
                <url></url>
                <content></content>
            </result>
            <result>
                <title></title>
                <url></url>
                <content></content>
            </result>
        </search_results>

        Here are the internet_search_results:
        {self.xml_parser.search_results_to_xml(search_results)}

        Here is the users prompt:
        <query>{query}</query>
        """
        return self.bedrock_client.query_model(model, prompt)