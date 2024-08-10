import json
from SearchResults import SearchResults
from FoundationalModel import FoundationalModel
from BedrockClient import BedrockClient
from PreProcessingAgent import PreProcessingAgent
from InternetSearchAgent import InternetSearchAgent
from ResponseAgent import ResponseAgent

def _parse_model(model_string: str) -> FoundationalModel:
    model_mapping = {
        "CLAUDE_35_SONNET": FoundationalModel.CLAUDE_35_SONNET,
        "CLAUDE_3_OPUS": FoundationalModel.CLAUDE_3_OPUS,
        'CLAUDE_3_SONNET': FoundationalModel.CLAUDE_3_SONNET,
        'CLAUDE_#_HAIKU': FoundationalModel.CLAUDE_3_HAIKU,
        'LLAMA_3.1_70b': FoundationalModel.LLAMA_31_70B,
        "LLAMA_3.1_8b": FoundationalModel.LLAMA_31_8B
    }

    if model_string.upper() not in model_mapping:
        raise ValueError(f"Unsupported model type: {model_string}")
    
    return model_mapping[model_string.upper()]
    

def handler(event, context):
    user_query = str(event['query'])
    selected_model = _parse_model(str(event['model']))

    bedrock_client = BedrockClient()
    preprocessing_agent = PreProcessingAgent(bedrock_client)
    internet_plugin_agent = InternetSearchAgent()
    response_agent = ResponseAgent(bedrock_client)

    try:
        search_params = preprocessing_agent.process(user_query, FoundationalModel.CLAUDE_3_HAIKU)
        
        if search_params.use_internet:
            print("Searching Internet")
            search_results = internet_plugin_agent.search(search_params.search_query)
        else:
            print("Internet Search Not Needed")
            search_results = SearchResults([])

        print(f"Querying: {selected_model.name}")
        final_answer = response_agent.generate_response(user_query, selected_model, search_results)
        print(f"Answer returned from: {selected_model.name}")

        return {
            'statusCode': 200,
            'body': {
                'answer': final_answer
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }