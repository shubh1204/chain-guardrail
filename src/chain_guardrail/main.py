from langchain_core.messages import AIMessage

from src.chain_guardrail.pii.presidio.parser_pii import parse_text


class ChainValidator:
    def __init__(self):
        self.anonymizer_dict = {}

    def static_validator(self, ai_message: AIMessage) -> str:
        """Parse the AI message."""
        filtered_text, anonymizer_dict = parse_text(ai_message.content)
        self.anonymizer_dict = anonymizer_dict
        print(f'Anonymizer dict:\n {anonymizer_dict}')
        return filtered_text
