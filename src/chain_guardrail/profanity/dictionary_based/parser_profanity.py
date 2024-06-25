with open('bad_words.txt') as f:
    bad_words = f.read().splitlines()


def parse_text(text: str) -> tuple[str, dict]:
    anonymizer_dict = {}
    bad_words_processed = 0
    processed_entities = []

    for word in bad_words:
        if word in text:
            if word in processed_entities:
                continue
            bad_words_processed += 1
            anonymizer_dict[word] = f'<Bad Word{bad_words_processed}>'
            processed_entities.append(word)

    for key, value in anonymizer_dict.items():
        text = text.replace(key, value)

    return text, {v: k for k, v in anonymizer_dict.items()}


print(parse_text("4r5e hole"))
