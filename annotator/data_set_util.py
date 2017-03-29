RADIO_TRAIN = 8
RADIO_TEST = 1
RADIO_DEV = 1
SUM_RADIO = RADIO_TRAIN + RADIO_TEST + RADIO_DEV
RADIO_DATA_SET = [RADIO_TRAIN, RADIO_TRAIN + RADIO_TEST, SUM_RADIO]


def get_data_set_group(index):
    t = index % SUM_RADIO
    for i in range(0, 3):
        if t < RADIO_DATA_SET[i]:
            return i
    return 0


def build_conll_fomat_for_sentence(words, tags):
    return '\n'.join('%s\t%s' % (w, y) for w, y in zip(words, tags))


def build_html_fomat_for_sentence(words, tags):
    current_tag = None
    current_tag_content = []
    new_words = []
    for word, tag in zip(words, tags):
        if tag == 'O':
            if current_tag and current_tag_content:
                new_words.append("<{current_tag}>{current_tag_content}</{current_tag}>".format(
                    current_tag=current_tag, current_tag_content=" ".join(current_tag_content)))
                current_tag = None
                current_tag_content = []
            new_words.append(word)
        else:
            if tag.startswith('B-'):
                if current_tag and current_tag_content:
                    new_words.append("<{current_tag}>{current_tag_content}</{current_tag}>".format(
                        current_tag=current_tag, current_tag_content=" ".join(current_tag_content)))
                    current_tag = None
                    current_tag_content = []
                current_tag = tag[2:]
                current_tag_content.append(word)
            if tag.startswith('I-'):
                current_tag_content.append(word)

    return " ".join(new_words)


def build_conll_fomat_for_sentences(words_list, tags_list):
    return "\n\n".join([build_conll_fomat_for_sentence(words, tags) for words, tags in zip(words_list, tags_list)])


def build_html_fomat_for_sentences(words_list, tags_list):
    return "\n\n".join([build_html_fomat_for_sentence(words, tags) for words, tags in zip(words_list, tags_list)])
