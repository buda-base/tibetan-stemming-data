from PyTib import getSylComponents
from PyTib.common import open_file, write_file
import re

def contains_sskrt(syl):
    # Source for regexes : Paul Hackett Visual Basic script
    # Now do Sanskrit: Skt.vowels, [g|d|b|dz]+_h, hr, shr, Skt
    regex1 = r"([ཀ-ཬཱ-྅ྐ-ྼ]{0,}[ཱཱཱིུ-ཹཻཽ-ྃ][ཀ-ཬཱ-྅ྐ-ྼ]{0,}|[ཀ-ཬཱ-྅ྐ-ྼ]{0,}[གཌདབཛྒྜྡྦྫ][ྷ][ཀ-ཬཱ-྅ྐ-ྼ]{0,}|[ཀ-ཬཱ-྅ྐ-ྼ]{0,}[ཤཧ][ྲ][ཀ-ཬཱ-྅ྐ-ྼ]{0,}|[ཀ-ཬཱ-྅ྐ-ྼ]{0,}[གྷཊ-ཎདྷབྷཛྷཥཀྵ-ཬཱཱཱིུ-ཹཻཽ-ྃྒྷྚ-ྞྡྷྦྷྫྷྵྐྵ-ྼ][ཀ-ཬཱ-྅ྐ-ྼ]{0,})"
    # more Sanskrit: invalid superscript-subscript pairs
    regex2 = r"([ཀ-ཬཱ-྅ྐ-ྼ]{0,}[ཀཁགང-ཉཏ-དན-བམ-ཛཝ-ཡཤཧཨ][ྐ-ྫྷྮ-ྰྴ-ྼ][ཀ-ཬཱ-྅ྐ-ྼ]{0,})"
    # tsa-phru mark used in Chinese transliteration
    regex3 = r"([ཀ-ཬཱ-྅ྐ-ྼ]{0,}[༹][ཀ-ཬཱ-྅ྐ-ྼ]{0,})"
    is_sskrt = False
    if not re.search(regex1, syl) or not re.search(regex2, syl) or not re.search(regex3, syl):
        is_sskrt = True
    return is_sskrt


components = getSylComponents()
components.dadrag = open_file('dadrag_syllables.txt').strip().split('\n')
tsikchen = open_file('./vocabs/TDC.txt').strip().split('\n')

# manually obtained by filtering the output of line 43
affixable_sskrt = ['ཀཱ', 'ཀཱ', 'ཡཿ', 'ཀཱ', 'ཊ', 'ཊ', 'ཀལྤ', 'ཏུཿ', 'ཊ', 'ཥ', 'ཤམབྷི', 'ཀཝ', 'ཁཎཌ', 'གཱ', 'གཎཌི', 'སཧྲཱི', 'ལཱ', 'ཤིརཥ', 'ཥ', 'ཊིཀ', 'དཧྲུ', 'ཊཱིཀ', 'ཐརྐ', 'ལྡེའུ', 'རཿ', 'ཊ', 'ཊུ', 'ཎཾ', 'པདམ', 'ཥ', 'པྲེཏཱ', 'བནདེ', 'བིལྦ', 'བེརྒ', 'ཋ', 'ཎི', 'ཊི', 'གྷ', 'མཉཛུ', 'ཥཱན', 'མརྒཏ', 'མརྒད', 'མཧཱ', 'མཧཱམཱཡཿ', 'མཱལཏི', 'ཀཱ', 'མིཏྲཱི', 'དམེའ', 'བྱཱ', 'ཙཀྲ', 'ལཱི', 'ཙནདྲ', 'ཊ', 'པདམ', 'ཡནཏུ', 'ཛཱཔཱ', 'ཥཐ', 'ཎ', 'སཱི', 'ཝརྟུ', 'དཧྲུ', 'ལཱ', 'གཱི', 'ཊི', 'རཀཏ', 'རཀཤ', 'རཏན', 'རཏནབྷདྲ', 'ཀཱ', 'བྷ', 'ཥི', 'ཊ', 'ཋ', 'ལཱ', 'ལཉཚ', 'ལཉཛ', 'བཱི', 'ལིངག', 'པཎ', 'ལོཀེཤྭརཿ', 'བྷ', 'ཤཱཀྱ', 'ཎ', 'ཁཎཊ', 'ལེནདྲ', 'ཏསྐྲ', 'སེདྷ', 'དྷ', 'གྷ', 'སརྦ', 'ཊ', 'ཏཱ', 'སུརཡ', 'སུརཡ', 'ཊཾ', 'དྷུ', 'བཛར', 'ཐཱ', 'ཨུཏཔལ']

lexicon = []
for word in tsikchen:
    syls = word.strip('་').split('་')
    # add /C to all syllables that are within dadrag_syllables.txt
    for p in range(len(syls)):
        if components.get_info(syls[p]) == 'dadrag':
            syls[p] += '/C'

    # add either /A or /B if the word ends with a thame
    if '/' not in syls[-1]:
        if components.is_thame(syls[-1]):
            if syls[-1].endswith('འ'):
                syls[-1] += '/A'
            else:
                syls[-1] += '/B'
        elif components.get_parts(syls[-1]) == None and contains_sskrt(syls[-1]):
            #  # used to print all the syllables and manually select the ones that allow an affixed particle
            # print(syls[-1], end = ' ')
            if syls[-1] in affixable_sskrt:
                syls[-1] += '/B'

    # reinsert the tseks
    for s in range(len(syls)-1):
        if '/' not in syls[s] and syls[s].endswith('ཿ'):
            continue
        elif '/' not in syls[s]:
            syls[s] += '་'
        else:
            syls[s] = '་/'.join(syls[s].split('/'))

    lexicon.append(''.join(syls))
write_file('lexicon_with_markers.txt', '\n'.join(lexicon))