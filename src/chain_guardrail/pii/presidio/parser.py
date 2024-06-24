from presidio_analyzer import AnalyzerEngine


def parse_text(text: str) -> tuple[str, dict]:
    anonymizer_dict = {}
    entity_count_dict = {}
    processed_entities = []

    analyzer = AnalyzerEngine()
    # replace "'" with space to be able to detect names, will revert back when final output
    transformed_text = text.replace("'", " ")
    results = analyzer.analyze(text=transformed_text, language="en", score_threshold=0.4)

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

# print(parse_text(text="Aria' el Bright and Ismael are trying his best to do it. But Aria' el Bright is not that good!"))
