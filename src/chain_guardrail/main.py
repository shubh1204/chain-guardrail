from langchain_core.messages import AIMessage
from langchain_community.chat_models import ChatOllama

from chain_guardrail.pii.presidio.parser import parse_text


class ChainValidator:
    def __init__(self):
        self.validation_result = []

    def static_validator(self, ai_message: AIMessage) -> str:
        """Parse the AI message."""
        result = parse_text(ai_message.content)
        self.validation_result = result.items
        return result.text

