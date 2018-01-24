import re

__MATCH__ = re.compile("(_lc[0-9]+_)[ ]")


def update_code_continue_problem_for_text(text):
    return re.sub(__MATCH__, r'\1\n', text)
