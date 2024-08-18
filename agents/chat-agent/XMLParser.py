import xml.etree.ElementTree as ET
from PreProcessingAgentResponse import PreProcessingAgentResponse

class XMLParser:
    @staticmethod
    def parse_preprocessing_agent_response(xml_str: str):
        root = ET.fromstring(xml_str)
        use_internet = bool(root.find('use_internet').text)
        search_query = str(root.find('search_query').text) if use_internet else None
        return PreProcessingAgentResponse(use_internet, search_query)

    @staticmethod
    def search_results_to_xml(search_results):
        root = ET.Element('search_results')
        for result in search_results.results:
            result_elem = ET.SubElement(root, 'result')
            ET.SubElement(result_elem, 'title').text = result['title']
            ET.SubElement(result_elem, 'url').text = result['url']
            ET.SubElement(result_elem, 'content').text = result['content']
        return ET.tostring(root, encoding='unicode')
