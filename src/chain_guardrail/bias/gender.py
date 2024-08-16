# Use a pipeline as a high-level helper
from transformers import pipeline


def toxicity_parser(text: str, toxicity_pipeline: pipeline) -> tuple[str, dict]:
    anonymizer_dict = {}
    statements = text.split('. ')
    processed_statements = 1
    for statement in statements:
        statement = statement.strip(' ').strip('\n')
        result = toxicity_pipeline(statement)
        # pred = get_prediction(result)
        # TODO: add threshold condition as well
        if get_prediction(result) == 'BIASED':
            text = text.replace(statement, f'<BIASED{processed_statements}>')
            anonymizer_dict[statement] = f'<BIASED{processed_statements}>'
            processed_statements += 1
    for key, value in anonymizer_dict.items():
        text = text.replace(key, value)
    return text, {v: k for k, v in anonymizer_dict.items()}


def get_prediction(result):
    if result[0]['label'] == 'NEUTRAL':
        if result[0]['score'] < 0.45:
            return 'NEUTRAL'
    return 'BIASED'


# pipe = pipeline("text-classification", model="D1V1DE/bias-detection", device='mps')
# print(toxicity_parser("Women are bad at driving", pipe))
