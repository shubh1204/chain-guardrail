import copy
import re

from chain_guardrail.profanity.bad_words_list import bad_words


def profanity_parser(text: str) -> tuple[str, dict]:
    bad_words_sorted = sorted(bad_words, key=len, reverse=True)
    anonymizer_dict = {}
    bad_words_processed = 1
    processed_entities = []
    text_copy_with_case = copy.deepcopy(text)
    text_copy = copy.deepcopy(text).lower()
    # # removing special characters for fixed pattern matching -- required??
    # text_copy = ''.join(e for e in text_copy if e.isalnum() or e in [' ', '<', '>'])

    # TODO: if 2 words detected between same index slice, handle it
    for word in bad_words_sorted:
        if word in text_copy:
            indices = [m.start() for m in re.finditer(word, text_copy)]
            for index in indices:
                word_in_original_text = text_copy_with_case[index:index + len(word)]
                text_copy_with_case = text_copy_with_case.replace(word_in_original_text, '')

                if word_in_original_text in anonymizer_dict:
                    pass
                else:
                    anonymizer_dict[word_in_original_text] = f'<BAD_WORD{bad_words_processed}>'
                    bad_words_processed += 1
                    processed_entities.append(word_in_original_text)
                    text_copy = text_copy.replace(word, '')

            # if word in processed_entities:
            #     continue
            # bad_words_processed += 1
            # anonymizer_dict[word] = f'<BAD_WORD{bad_words_processed}>'
            # processed_entities.append(word)
            # text_copy = text_copy.replace(word, '')

    for key, value in anonymizer_dict.items():
        text = text.replace(key, value)

    return text, {v: k for k, v in anonymizer_dict.items()}

# print(profanity_parser("4r5e hole"))
