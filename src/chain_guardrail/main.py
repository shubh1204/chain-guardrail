from langchain_core.messages import AIMessage
from transformers import pipeline
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

from src.chain_guardrail.pii.presidio_pii import pii_parser
from src.chain_guardrail.profanity.fixed_pattern import profanity_parser
from src.chain_guardrail.toxicity.large import toxicity_parser


class ChainValidator:
    def __init__(self):
        print('Loading Model ...')
        # TODO: load model on gpu if available
        self.toxicity_pipe = pipeline("text-classification", model="textdetox/xlmr-large-toxicity-classifier")
        self.gender_bias_pipe = pipeline("text-classification", model="monologg/koelectra-base-gender-bias")

        # load spacy trf model
        # Create configuration containing engine name and models
        configuration = {
            "nlp_engine_name": "spacy",
            "models": [{"lang_code": "en", "model_name": "en_core_web_trf"}],
        }

        # Create NLP engine based on configuration
        provider = NlpEngineProvider(nlp_configuration=configuration)
        nlp_engine = provider.create_engine()

        # Pass the created NLP engine and supported_languages to the AnalyzerEngine
        self.presidio_pii_pipe = AnalyzerEngine(
            nlp_engine=nlp_engine,
            supported_languages=["en"]
        )

        print('Model Loaded ...')
        self.anonymizer_dict = {}

    def static_validator(self, ai_message: AIMessage) -> tuple[str, dict]:
        """Parse the AI message."""
        filtered_text, anonymizer_dict = pii_parser(ai_message.content, self.presidio_pii_pipe)
        self.anonymizer_dict['pii'] = anonymizer_dict

        filtered_text, anonymizer_dict = toxicity_parser(filtered_text, self.toxicity_pipe)
        self.anonymizer_dict['toxicity'] = anonymizer_dict

        filtered_text, anonymizer_dict = profanity_parser(filtered_text)
        self.anonymizer_dict['profanity'] = anonymizer_dict

        return filtered_text, self.anonymizer_dict
