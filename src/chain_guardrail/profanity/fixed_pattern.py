import copy

from chain_guardrail.profanity.bad_words_list import bad_words


def profanity_parser(text: str) -> tuple[str, dict]:
    anonymizer_dict = {}
    bad_words_processed = 0
    processed_entities = []
    text_copy = copy.deepcopy(text)

    for word in bad_words:
        if word in text_copy:
            if word in processed_entities:
                continue
            bad_words_processed += 1
            anonymizer_dict[word] = f'<BAD_WORD{bad_words_processed}>'
            processed_entities.append(word)
            text_copy = text_copy.replace(word, '')

    for key, value in anonymizer_dict.items():
        text = text.replace(key, value)

    return text, {v: k for k, v in anonymizer_dict.items()}

# print(profanity_parser("4r5e hole"))
