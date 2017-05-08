from utils import open_file, write_file, collator

verbs_raw = open_file('output/parsed_verbs.txt')
verbs = [tuple(a.split(' ')) for a in verbs_raw.strip().split('\n')]

particles_raw = open_file('input/particles.txt')
particles = [tuple(a.split(' ')) for a in particles_raw.strip().split('\n')]

lexicon_raw = open_file('output/lexicon_with_markers.txt')
lexicon = lexicon_raw.strip().split('\n')
A_expansion = {'འི': '>A', 'འོ': '>B', 'ས': '>C', 'ར': '>D', 'འའིས': '>E'}
B_expansion = {'འི': '>a', 'འོ': '>b', 'ས': '>c', 'ར': '>d'}
# operations to reconstruct the lemma
cmds = {'>A': ('-འི', '+འ'),
        '>a': ('-འི',),
        '>B': ('-འོ', '+འ'),
        '>b': ('-འོ',),
        '>C': ('-ས', '+འ'),
        '>c': ('-ས',),
        '>D': ('-ར', '+འ'),
        '>d': ('-ར',),
        '>E': ('-འའིས', '+འ')
        }

lexicon_expanded = []
for word in lexicon:
    base_form = word.replace('/A', '').replace('/B', '').replace('/C', '')
    if base_form == 'ཀུན་དགའ':
        print('ok')
    # expand all forms with dadrag
    with_dadrag = []
    if '/C' in word:
        with_dadrag.append(word.replace('/C', ''))
        with_dadrag.append(word.replace('་/C', 'ད་'))
    else:
        with_dadrag.append(word)

    # expand the forms that can have affixed particles
    with_affixed = []
    for form in with_dadrag:
        if '/' in form:
            to_affix, kind = form.split('/')
            if kind == 'A':
                with_affixed.append((to_affix, '='))
                to_affix = to_affix.rstrip('འ')
                for affix in sorted(A_expansion):
                    with_affixed.append((to_affix + affix, A_expansion[affix]))
            if kind == 'B':
                with_affixed.append((to_affix, '='))
                for affix in sorted(B_expansion):
                    with_affixed.append((to_affix + affix, B_expansion[affix]))
        else:
            with_affixed.append((form, '='))

    # fill lexicon_expanded with all the forms found
    lexicon_expanded.extend(with_affixed)
    # for final in with_affixed:
    #     lexicon_expanded.append((final, base_form))

# merge all lists de-duplicating
total_entries = list(set(lexicon_expanded+verbs+particles))

tib_sorted = sorted(total_entries, key=lambda x: collator.getSortKey(x[0]))
lines = ['{} {}'.format(inflected, cmd) for inflected, cmd in tib_sorted]
write_file('output/total_lexicon.txt', '\n'.join(lines))