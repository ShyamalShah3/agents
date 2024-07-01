from enum import Enum

class FoundationalModel(Enum):
    CLAUDE_3_SONNET = ("Claude 3 Sonnet", "anthropic.claude-3-sonnet-20240229-v1:0", 1.0, 4096)
    CLAUDE_3_HAIKU = ("Claude 3 Haiku", "anthropic.claude-3-haiku-20240307-v1:0", 1.0, 4096)
    LLAMA_3_70B = ("Llama 3 70B", "meta.llama3-70b-instruct-v1:0", 1.0, 2048)
    LLAMA_3_8B = ("Llama 3 8B", "meta.llama3-8b-instruct-v1:0", 0.5, 2048)

    def __init__(self, model_name, model_id, model_temperature, model_max_tokens):
        self.model_name = model_name
        self.model_id = model_id
        self.model_temperature = model_temperature
        self.model_max_tokens = model_max_tokens
