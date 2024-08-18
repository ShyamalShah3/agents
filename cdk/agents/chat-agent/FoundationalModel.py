from enum import Enum

class FoundationalModel(Enum):
    CLAUDE_35_SONNET = ("Claude 3.5 Sonnet", "anthropic.claude-3-5-sonnet-20240620-v1:0", 0.7, 8192)
    CLAUDE_3_OPUS = ("Claude 3 Opus", "anthropic.claude-3-opus-20240229-v1:0", 0.7, 4096)
    CLAUDE_3_SONNET = ("Claude 3 Sonnet", "anthropic.claude-3-sonnet-20240229-v1:0", 1.0, 4096)
    CLAUDE_3_HAIKU = ("Claude 3 Haiku", "anthropic.claude-3-haiku-20240307-v1:0", 1.0, 4096)
    LLAMA_31_70B = ("Llama 3.1 70B", "meta.llama3-1-70b-instruct-v1:0", 0.7, 2048)
    LLAMA_31_8B = ("Llama 3.1 8B", "meta.llama3-1-8b-instruct-v1:0", 0.7, 2048)

    def __init__(self, model_name, model_id, model_temperature, model_max_tokens):
        self.model_name = model_name
        self.model_id = model_id
        self.model_temperature = model_temperature
        self.model_max_tokens = model_max_tokens
