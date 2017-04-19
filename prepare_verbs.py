import jsonpickle as jp
from collections import defaultdict
from PyTib.common import open_file, write_file, tib_sort

jp.set_encoder_options('simplejson', sort_keys=True, indent=4, ensure_ascii=False)

content = open_file('monlam_verbs.json')
json = jp.decode(content)

ambiguous_verbs = {}
non_ambiguous_verbs = {}
for inflected, context in json.items():
    # a few entries don't have any content in monlam_verbs.json and are filtered here
    # like : ལྷོགས་ | ༡བྱ་ཚིག 1. ༡བརྡ་རྙིང་། རློགས། 2. ཀློགས། that parses into "ལྷོགས": []
    if context == []:
        continue
    possible_verbs = []
    for verb in context:
        # inflected verbs
        if 'བྱ་ཚིག' in verb.keys():
            possible_verbs.append(verb['བྱ་ཚིག'])
        # non-inflected verbs (གཟུགས་མི་འགྱུར་བ།)
        else:
            possible_verbs.append(inflected)
    possible_verbs = list(set(possible_verbs))

    # if there is only one possibility
    if len(possible_verbs) == 1:
        non_ambiguous_verbs[inflected] = possible_verbs[0]
    else:
        non_ambiguous_verbs[inflected] = '0'
        ambiguous_verbs[inflected] = possible_verbs

all_verbs = []
for verb in tib_sort(list(non_ambiguous_verbs.keys())):
    all_verbs.append('{} {}'.format(verb, non_ambiguous_verbs[verb]))
write_file('parsed_verbs.txt', '\n'.join(all_verbs))

ambiguous_total = []
for verb in tib_sort(list(ambiguous_verbs.keys())):
    ambiguous_total.append('{} {}'.format(verb, ' '.join(ambiguous_verbs[verb])))
write_file('ambiguous_verbs.txt', '\n'.join(ambiguous_total))
