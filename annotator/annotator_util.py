from annotator.models import NamedEntityAnnotation
from annotator.query_util import get_annotation, get_post_tokenize_remove_tag_body_with_small_code_block


def get_need_tagged_text(post_id):
    annotation = get_annotation(post_id)
    if annotation:
        text = annotation.annotation_text
    else:
        text = get_post_tokenize_remove_tag_body_with_small_code_block(post_id)
    return text


def save_as_ner_annotation(post_id, text):
    annotation = get_annotation(post_id)
    if annotation:
        annotation.annotation_text = text
        annotation.save()
    else:
        annotation = NamedEntityAnnotation(id=post_id, annotation_text=text)
        annotation.save()


