from annotator.models import NamedEntityAnnotation, SentenceTypeAnnotation, Posts, SentenceType
from annotator.query_util import get_annotation, get_post_tokenize_remove_tag_body_with_small_code_block


def __init_sentence_type_list():
    try:
        __sentence_type_list__ = SentenceType.objects.all()  # the sentence type list
        if len(__sentence_type_list__) == 0:
            raise SentenceType.DoesNotExist
        return __sentence_type_list__
    except SentenceType.DoesNotExist:
        unknown_sentence_type = SentenceType(name='unknown', description='Difficult to classify sentences')
        unknown_sentence_type.save()
        return SentenceType.objects.all()


__sentence_type_list__ = __init_sentence_type_list()


def get_need_tagged_text(post_id):
    annotation = get_annotation(post_id)
    if annotation:
        text = annotation.annotation_text
    else:
        text = get_post_tokenize_remove_tag_body_with_small_code_block(post_id)
    return text


def get_sentence_tye_annotations(post_id):
    try:
        sentence_tye_annotations = SentenceTypeAnnotation.objects.filter(post_id=post_id).order_by('sentence_index')
        if len(sentence_tye_annotations) == 0:
            raise Exception
        return sentence_tye_annotations

    except Exception:
        try:
            post = Posts.objects.get(id=post_id)
            text = get_post_tokenize_remove_tag_body_with_small_code_block(post_id)
            sentences = text.split('\n')
            for i in range(len(sentences)):
                annotation = SentenceTypeAnnotation(post=post,
                                                    sentence_type=__sentence_type_list__[0],
                                                    sentence_index=i,
                                                    annotation_text=sentences[i])
                annotation.save()
            sentence_tye_annotations = SentenceTypeAnnotation.objects.filter(post_id=post_id).order_by('sentence_index')
            return sentence_tye_annotations
        except:
            return None


def save_as_ner_annotation(post_id, text):
    annotation = get_annotation(post_id)
    if annotation:
        annotation.annotation_text = text
        annotation.save()
        print 'save annotation for id=', annotation.id

    else:
        annotation = NamedEntityAnnotation(id=post_id, annotation_text=text)
        annotation.save()
        print 'save annotation for id=', annotation.id
