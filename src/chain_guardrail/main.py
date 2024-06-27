from langchain_core.messages import AIMessage

from chain_guardrail.pii.presidio_pii import pii_parser
from chain_guardrail.profanity.fixed_pattern import profanity_parser


class ChainValidator:
    def __init__(self):
        self.anonymizer_dict = {}

    def static_validator(self, ai_message: AIMessage) -> tuple[str, dict]:
        """Parse the AI message."""
        filtered_text, anonymizer_dict = pii_parser(ai_message.content)
        self.anonymizer_dict['pii'] = anonymizer_dict

        filtered_text, anonymizer_dict = profanity_parser(filtered_text)
        self.anonymizer_dict['profanity'] = anonymizer_dict

        # print(f'Anonymizer dict:\n {self.anonymizer_dict}')
        return filtered_text, self.anonymizer_dict
