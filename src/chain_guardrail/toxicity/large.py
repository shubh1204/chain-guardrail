# Use a pipeline as a high-level helper
from transformers import pipeline


def toxicity_parser(text: str, toxicity_pipeline: pipeline) -> tuple[str, dict]:
    anonymizer_dict = {}
    statements = text.split('. ')
    processed_statements = 1
    for statement in statements:
        statement = statement.strip(' ').strip('\n')
        result = toxicity_pipeline(statement)
        # TODO: add threshold condition as well
        if result[0]['label'] == 'toxic':
            text = text.replace(statement, f'<TOXIC{processed_statements}>')
            anonymizer_dict[statement] = f'<TOXIC{processed_statements}>'
            processed_statements += 1
    for key, value in anonymizer_dict.items():
        text = text.replace(key, value)
    return text, {v: k for k, v in anonymizer_dict.items()}


# pipe = pipeline("text-classification", model="textdetox/xlmr-large-toxicity-classifier")
# print(toxicity_parser("Dis hoe wasnt dis violent on Lottery Ticket ðŸ˜‚ðŸ˜‚", pipe))
