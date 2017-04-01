import codecs
import os

from annotator.data_set_util import get_data_set_group
from SOKnowledge.ner_util.format_util import build_conll_format_for_sentences
from annotator.label_data_builder import build_code_tagger_data_for_sentence, build_code_tagger_data_for_whole_post
from annotator.query_util import get_question_list, get_post_text, \
    get_all_code_block, get_all_answer, POST_TEXT_TYPE_TOKENIZE_NO_CODE_BLOCK


def get_post_code_block_type_str(code_block_type):
    if code_block_type < 0:
        return 'full_tag'
    if code_block_type == 0:
        return 'only_small'
    return 'unkonwn'


def export_code_block_ner_data_set_by_step(
        start=0,
        max_num=1000,
        step=100,
        post_text_type=-1,
        output_file_path=".",
        output_file_name="code_block_ner.txt"):
    for offset in range(start, max_num, step):
        export_code_block_ner_data_set(num=step, offset=offset, post_text_type=post_text_type,
                                       output_file_path=output_file_path, output_file_name=output_file_name)
        print 'done', offset, '-', offset + step


def export_code_block_ner_data_set(
        num=100,
        offset=0,
        post_text_type=-1,
        output_file_path=".",
        output_file_name="code_block_ner.txt"):
    output_file_name = '{0}_{1}_{2}_{3}'.format(str(offset), str(offset + num),
                                                get_post_code_block_type_str(post_text_type), output_file_name)

    train_output_file_name = "train_" + output_file_name
    test_output_file_name = "test_" + output_file_name
    dev_output_file_name = "dev_" + output_file_name
    count_questions = [0, 0, 0]
    count_answers = [0, 0, 0]

    with codecs.open(os.path.join(output_file_path, train_output_file_name), 'w', encoding='utf-8') as train_output:
        with codecs.open(os.path.join(output_file_path, test_output_file_name), 'w', encoding='utf-8') as test_output:
            with codecs.open(os.path.join(output_file_path, dev_output_file_name), 'w', encoding='utf-8') as dev_output:
                output_file_list = [train_output, test_output, dev_output]
                question_list = get_question_list(offset=offset, num=num)
                question_num = 0
                for question in question_list:
                    words_list = []
                    tags_list = []
                    group = get_data_set_group(question_num)
                    output = output_file_list[group]
                    if question.title:
                        title_words, title_tags = build_code_tagger_data_for_sentence(question.title, [])
                        words_list.append(title_words)
                        tags_list.append(title_tags)
                    get_code_block_tag_for_one_post(question, post_text_type, tags_list, words_list)

                    answer_list = get_all_answer(question.id)
                    if answer_list:
                        answer_count = answer_list.count()
                    else:
                        answer_count = 0
                    for answer in answer_list:
                        get_code_block_tag_for_one_post(answer, post_text_type, tags_list, words_list)
                    output.write(build_conll_format_for_sentences(words_list, tags_list))
                    output.write("\n\n")
                    question_num += 1
                    count_questions[group] += 1

                    if answer_count > 0:
                        count_answers[group] += answer_count
    output_count_info(count_answers, count_questions, output_file_name, output_file_path, question_num)


def output_count_info(count_answers, count_questions, output_file_name, output_file_path, question_num):
    with codecs.open(os.path.join(output_file_path, 'count_' + output_file_name), 'w',
                     encoding='utf-8') as count_output:
        count_output.write('question_num=' + str(question_num) + '\n')
        count_output.write('train   test    dev' + '\n')

        count_output.write('count_questions:' + '\n')
        write_list(count_output, count_questions)

        count_output.write('\n\n')
        count_output.write('count_answers:' + '\n')
        write_list(count_output, count_answers)
        count_output.write('\n\n')


def write_list(count_output, my_list):
    for t in my_list:
        count_output.write(str(t))
        count_output.write('\t')
    count_output.write('\n')


def get_code_block_tag_for_one_post(post, code_block_type, tags_list, words_list):
    post_text = get_post_text(post, POST_TEXT_TYPE_TOKENIZE_NO_CODE_BLOCK)
    if post_text:
        new_words_list, new_tags_list = build_code_tagger_data_for_whole_post(post_text,
                                                                              get_all_code_block(
                                                                                  post.id, code_block_type))
        words_list.extend(new_words_list)
        tags_list.extend(new_tags_list)
