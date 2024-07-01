class PreProcessingAgentResponse:
    def __init__(self, use_internet: bool, search_query: str = None):
        self.use_internet = use_internet
        self.search_query = search_query