import jsonpickle as jp
from utils import open_file, write_file, collator

jp.set_encoder_options('simplejson', sort_keys=True, indent=4, ensure_ascii=False)

content = open_file('input/monlam_verbs.json')
json = jp.decode(content)
dadrag = open_file('input/dadrag_syllables.txt').strip().split('\n')

entries = []
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


    # de-duplicate the verbs
    possible_verbs = list(set(possible_verbs))

    # add an entry for every possible verb
    if inflected in dadrag:
        for verb in possible_verbs:
            entries.append((inflected+'ད', verb))
    else:
        for verb in possible_verbs:
            if inflected == verb:
                entries.append((inflected, '='))
            else:
                entries.append((inflected, verb))

tib_sorted = sorted(entries, key=lambda x: collator.getSortKey(x[0]))
lines = ['{} {}'.format(inflected, lemma) for inflected, lemma in tib_sorted]
write_file('output/parsed_verbs.txt', '\n'.join(lines))
