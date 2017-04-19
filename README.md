# Data for testing the Tibetan Lucene analyzers

## affixify.py

 - Adds a /C to every encountered syllable that is in dadrag_syllables.txt. (its content comes from [here](https://github.com/eroux/tibetan-spellchecker/blob/master/doc/second-suffix-da.md). All syllables until GT are included)
 - To the final syllable:
    - nothing added if the syllable can't host any affixed particle,
    - /A added if the particle can host an affixed particle and requires a final འ to be valid,
    - /B added if the particle can host an affixed particle but doesn't require a འ. 

## prepare_verbs.py

Takes as input monlam_verbs.json, produced for Esukhia's canon_notes project and produces two files:
- parsed_verbs.txt contains all the inflected forms from Monlam. Each entry contains:
    - either the inflected form followed by the corresponding verb form, if it corresponds to a single verb
    - or the inflected forme followed by "0" in case the inflected form corresponds to more than one verb
- ambiguous_verbs.txt contains all the inflected forms that correspond to more than one verb, with the same format as above.

note: a few entries for which Monlam doesn't give any information about conjugation are ignored. (ex: ལྷོགས་ | ༡བྱ་ཚིག 1. ༡བརྡ་རྙིང་། རློགས། 2. ཀློགས།)

## small testing-set
test_sentence.txt contains the beginning  of a sutra split in words.

test_vocab.txt contains the words of that sentence categorised according to their syllable type:

## The whole tagged lexicon 
lexicon_with_markers.txt is obtained by processing vocabs/TDC.txt with affixify.py
note: the sskrt syllables marked with /B were manually processed. Ideally, a thorough analysis of sskrt syllables would enable to automatize this process.

