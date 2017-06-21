#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils import open_file, write_file, collator
import re
from itertools import product

verbs_raw = open_file('output/parsed_verbs.txt')
verbs = [tuple(a.split(' ')) for a in verbs_raw.strip().split('\n')]

particles_raw = open_file('input/particles.txt')
particles = [tuple(a.split(' ')) for a in particles_raw.strip().split('\n')]

lexicon_raw = open_file('output/lexicon_with_markers.txt')
lexicon = lexicon_raw.strip().split('\n')
A_expansion = {'འི': '>A', 'འོ': '>A', 'ས': '>D', 'ར': '>D', 'འའིས': '>C'}
B_expansion = {'འི': '>B', 'འོ': '>B', 'ས': '>A', 'ར': '>A', 'འིས': '>C'}
# operations to reconstruct the lemma
cmds = {'>A': ('-1',),
        '>B': ('-2',),
        '>C': ('-3',),
        '>D': ('-1', '+འ')
        }


def apply_cmds(form, cmd, cmds):
    to_apply = cmds[cmd]
    for mod in to_apply:
        if mod.startswith('-'):
            form = form[:len(form)-int(mod[1])]
        if mod.startswith('+'):
            form = form+mod[1:]
    return form


def generate_combinations(word):
    parts = [a for a in re.split('(་?/C)', word) if a != '']
    amount = word.count('/C')
    if amount == 2:
        permutations = list(product([0, 1], [0, 1]))
    if amount == 3:
        permutations = list(product([0, 1], [0, 1], [0, 1]))
    if amount == 4:
        permutations = list(product([0, 1], [0, 1], [0, 1], [0, 1]))
    total = []
    for per in permutations:
        temp = [a for a in parts]
        el_count = 1
        for choice in per:
            if choice == 1:
                if temp[el_count].startswith('་'):
                    temp[el_count] = 'ད་'
                else:
                    temp[el_count] = 'ད'
                el_count += 2
            elif choice == 0:
                temp[el_count] = temp[el_count].replace('/C', '')
                el_count += 2
        total.append(''.join(temp))
    return total

lexicon_expanded = []
for word in lexicon:
    base_form = word.replace('/A', '').replace('/B', '').replace('/C', '')
    if base_form == 'རྒྱབ་རྫི':
        print('ok')
    # expand all forms with dadrag
    with_dadrag = []
    if '/C' in word:
        if word.count('/C') > 1:
            with_dadrag.extend(generate_combinations(word))
        else:
            with_dadrag.append(word.replace('/C', ''))
            with_dadrag.append(re.sub(r'(་)?/C', r'ད\1', word))
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
                    if apply_cmds(to_affix+affix, A_expansion[affix], cmds) == base_form:
                        with_affixed.append((to_affix + affix, A_expansion[affix]))
                    else:
                        with_affixed.append((to_affix + affix, '/'+base_form))
            if kind == 'B':
                with_affixed.append((to_affix, '='))
                for affix in sorted(B_expansion):
                    if apply_cmds(to_affix+affix, B_expansion[affix], cmds) == base_form:
                        with_affixed.append((to_affix + affix, B_expansion[affix]))
                    else:
                        with_affixed.append((to_affix + affix, '/'+base_form))
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
print(len(total_entries))