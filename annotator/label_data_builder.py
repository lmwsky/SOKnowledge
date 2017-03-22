from SOKnowledge.data_processor.scripts.nlp_util import word_tokenize_nltk, sent_tokenize_nltk
from annotator.models import CodeBlockWithTokenizeCode


def get_code_block_object(code_block_name, code_block_list):
    """
    get the CodeBlockWithTokenizeCode object has the code_block_name
    :param code_block_name: the code_block_name need to match
    :param code_block_list: the CodeBlockWithTokenizeCode object
    :return: the CodeBlockWithTokenizeCode match the name
    """
    for code_block in code_block_list:
        if code_block_name == code_block.code_block_name:
            return code_block
    return None


def parse_to_tags_bio(text, tag_type):
    start_tag = "B-" + tag_type
    inside_tag = "I-" + tag_type
    tags = []
    words = text.split()
    if len(words) > 0:
        tags.append(start_tag)
        for i in range(1, len(words)):
            tags.append(inside_tag)
    return tags, words


def build_code_tagger_data_for_whole_post(tokenize_post_text, code_block_list):
    sentence_list = sent_tokenize_nltk(tokenize_post_text)
    sentence_words_list = []
    sentence_words_tags_list = []
    for sent in sentence_list:
        full_words, full_words_tags = build_code_tagger_data_for_sentence(sent, code_block_list)
        if full_words:
            sentence_words_list.append(full_words)
            sentence_words_tags_list.append(full_words_tags)
    return sentence_words_list, sentence_words_tags_list


def build_code_tagger_data_for_sentence(tokenize_post_sentence_text, code_block_list):
    words = word_tokenize_nltk(tokenize_post_sentence_text)

    full_words = []
    full_word_tags = []
    for word in words:
        code_block = get_code_block_object(word, code_block_list)
        if code_block:
            new_tags = []
            new_words = []
            if code_block.type == CodeBlockWithTokenizeCode.SMALL_CODE_BLOCK:
                new_tags, new_words = parse_to_tags_bio(code_block.tokenize_text, "SMALLCODE")
            elif code_block.type == CodeBlockWithTokenizeCode.LARGE_CODE_BLOCK:
                new_tags, new_words = parse_to_tags_bio(code_block.tokenize_text, "LARGECODE")
            full_word_tags.extend(new_tags)
            full_words.extend(new_words)
        else:
            full_word_tags.append("O")
            full_words.append(word)
    return full_words, full_word_tags


