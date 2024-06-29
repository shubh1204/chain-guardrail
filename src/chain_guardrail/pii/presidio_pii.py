import re

import spacy_transformers
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider


def pii_parser(text: str, analyzer: AnalyzerEngine) -> tuple[str, dict]:
    anonymizer_dict = {}
    entity_count_dict = {}
    processed_entities = []
    other_validators = re.findall(r'(TOXIC.+?)>', text)

    # analyzer = AnalyzerEngine()
    # replace "'" with space to be able to detect names, will revert back when final output
    transformed_text = text.replace("'", " ")
    results = analyzer.analyze(text=transformed_text, language="en", score_threshold=0.4, allow_list=other_validators)

    # Explicitly remove overlapping entities
    # currently taking the one which has larger window
    # TODO: verify this and update with threshold based insted if required, maybe add max of 0.15 threshold difference
    entities_to_remove = []
    for primary_entity in results:
        for secondary_entity in results:
            if primary_entity != secondary_entity and primary_entity.start >= secondary_entity.start and primary_entity.end <= secondary_entity.end:
                entities_to_remove.append(primary_entity)

    for entity in entities_to_remove:
        results.remove(entity)

    # count the number of entity type occurrence for each type
    for entity in results:

        entity_name = text[entity.start: entity.end]
        if entity.entity_type in entity_count_dict:
            if entity_name in processed_entities:
                continue
            else:
                entity_count_dict[entity.entity_type] += 1
        else:
            entity_count_dict[entity.entity_type] = 1

        processed_entities.append(entity_name)
        new_entity_type = f'{entity.entity_type}{entity_count_dict[entity.entity_type]}'
        anonymizer_dict[entity_name] = f'<{new_entity_type}>'

    for key, value in anonymizer_dict.items():
        text = text.replace(key, value)

    # return cleaned text and anonymizer mapping
    return text, {v: k for k, v in anonymizer_dict.items()}

#
# # Create configuration containing engine name and models
# configuration = {
#     "nlp_engine_name": "spacy",
#     "models": [{"lang_code": "en", "model_name": "en_core_web_trf"}],
# }
#
# # Create NLP engine based on configuration
# provider = NlpEngineProvider(nlp_configuration=configuration)
# nlp_engine = provider.create_engine()
#
# # Pass the created NLP engine and supported_languages to the AnalyzerEngine
# pipe = AnalyzerEngine(
#     nlp_engine=nlp_engine,
#     supported_languages=["en"]
# )
#
# print(pii_parser(
#     text="My name is Tjirrkarli Nullarbor and my mobile is +91-7053654462", analyzer=pipe))
