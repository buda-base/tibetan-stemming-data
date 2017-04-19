from PyTib import getSylComponents
from PyTib.common import open_file, write_file, tib_sort
import os

components = getSylComponents()
components.dadrag = open_file('dadrag_syllables.txt').strip().split('\n')
tsikchen = open_file('./vocabs/TDC.txt').strip().split('\n')
input_files = ['{}/{}'.format('vocabs', f) for f in os.listdir('vocabs') if f != '.git' and f != 'verbs']
input_files += ['{}/{}'.format('vocabs/verbs', f) for f in os.listdir('vocabs/verbs') if f != 'README.md']

lexicon = []
for f in input_files:
    content = open_file(f).strip().split('\n')
    for word in content:
        syls = word.strip('་').split('་')
        # add /C to all syllables that are within dadrag_syllables.txt
        for p in range(len(syls)):
            if components.get_info(syls[p]) == 'dadrag':
                syls[p] += '/C'

        # add either /A or /B if the word ends with a thame
        if components.is_thame(syls[-1]):
            if syls[-1].endswith('འ'):
                syls[-1] += '/A'
            else:
                syls[-1] += '/B'

        # reinsert the tseks
        for s in range(len(syls)-1):
            if '/' not in syls[s]:
                syls[s] += '་'
            else:
                syls[s] = '་/'.join(syls[s].split('/'))

        lexicon.append(''.join(syls))

write_file('lexicon_with_markers.txt', '\n'.join(tib_sort(list(set(lexicon)))))