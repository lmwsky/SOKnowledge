__labels__ = [
    {'textLabel': 'API',
     'description': 'one api in program,ex. Integer.parseInt()',
     'value': 'api',
     },
    {'textLabel': 'PLAT',
     'description': 'one platform,ex.Linux,android,Windows 10',
     'value': 'platform',
     },
    {'textLabel': 'Fram',
     'description': 'Frame used in program, ect.django,ionic, ',
     'value': 'frame',
     },
    {'textLabel': 'PL',
     'description': 'program language,ex.JAVA,C++',
     'value': 'language',
     },
    {'textLabel': 'Stan',
     'description': 'like http,xml',
     'value': 'standard',
     },
]


def parse_from_tag_format_to_se_format(text, label_list=__labels__):
    for label in label_list:
        start_tag = "<{0}>".format(label['textLabel'])
        replace_start_tag = "<START:{0}>".format(label['value'])
        end_tag = "</{0}>".format(label['textLabel'])
        replace_end_tag = "<END>".format(label['value'])
        text = text.replace(start_tag, replace_start_tag)
        text = text.replace(end_tag, replace_end_tag)
    return text


def parse_from_se_format_to_tag_format(text, label_list=__labels__):
    label_dict = {}
    for label in label_list:
        label_dict[label["value"]] = label["textLabel"]

    tag_start_pos = text.find("<START:", 0)
    while tag_start_pos >= 0:
        end_index = text.find('>', tag_start_pos)
        tag = text[tag_start_pos + 7:end_index]
        text = text.replace("START:" + tag, label_dict[tag], 1)
        text = text.replace("<END>", "</{0}>".format(label_dict[tag]), 1)
        tag_start_pos = text.find("<START:", tag_start_pos + 7)

    return text
