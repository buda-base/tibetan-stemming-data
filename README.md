# Data for testing the Tibetan Lucene analyzers

## Generated resources

##### `output/total_lexicon.txt`
A general purpose Tibetan word-list.
Each line is formatted as follows: `inflected<space>operation`
Affixed particles (འི, འོ, -ས and -ར) and dadrag (ད་དྲག) are appended to each processed word following the syllable-formation rules.

`operation` (to reconstruct the lemma) can have the following values:
  - `/lemma`: the lemma is inserted when more than the operations below are required to find it from the inflected form 
  - `=`: the inflected form and the lemma are identical
  - `>A`: remove one character 
  - `>B`: remove two characters
  - `>C`: remove three characters
  - `>D`: remove one character and add "འ"

##### Minimal testing-set
 - `test_sentence.txt`: the beginning of a sutra(བཀྲ་ཤིས་ཆེན་པོའི་མདོ།) split in words.
 - `test_vocab.txt`: the words from the sentence and all their inflected forms.

## `affixify.py`

##### Input:
 - `input/dadrag_syllables.txt` (from [here](https://github.com/eroux/tibetan-spellchecker/blob/master/doc/second-suffix-da.md). All syllables until GT are included)
 - `input/vocabs/TDC.txt` (from [here](https://github.com/Esukhia/Tibetan-NLP-Resources))

##### Action
 - To every entry of `TDC.txt`:
    - Appends /C to every syllable that is in `dadrag_syllables.txt` 
    - To the final syllable:
        - nothing added if the syllable can't host any affixed particle,
        - /A added if the particle can host an affixed particle and requires a final འ to be valid,
        - /B added if the particle can host an affixed particle but doesn't require a འ. 

##### Output
 - `output/lexicon_with_markers.txt`
 
##### Issues
 - the sskrt syllables marked with /B were manually processed. Implementing of the sskrt syllables formation rules would enable to automatize this process.

## `prepare_verbs.py`

##### Input
 - `input/monlam_verbs.json` (from Esukhia's [canon_notes](https://github.com/Esukhia/canon_notes/tree/code/2-automatic_categorisation/resources) project)
 - `input/dadrag_syllables.txt`

##### Action
 - for every inflected form:
    - find all the lemmas (citation forms)
    - create a second inflected form if the verb is in `dadrag_syllables.txt`
    - add `(inflected, /lemma)` to the output list (`=` instead of `/lemma` if the inflected form and the lemma are identical)

##### Output
 - `output/parsed_verbs.txt`

##### Issues
 - a few entries for which Monlam doesn't give any information about conjugation are ignored. (ex: `ལྷོགས་ | ༡བྱ་ཚིག 1. ༡བརྡ་རྙིང་། རློགས། 2. ཀློགས།` is parsed into `"ལྷོགས": []`)

## `compile_total_lexicon.py`

##### Input

- `output/parsed_verbs.txt`
- `input/particles.txt` (an adaptation of [this list](https://github.com/BuddhistDigitalResourceCenter/lucene-bo/blob/master/src/main/java/io/bdrc/lucene/bo/TibetanAnalyzer.java#L43))
- `output/lexicon_with_markers.txt`

##### Action
 - expands every entry in `lexicon_with_markers.txt`:
    - /C : create a new entry with a dadrag on the marked syllable
    - for the entry (or entries if there is one with dadrag):
        - /A : remove the ending འ
        - apply all affixes (`['འི', 'འོ', 'ས', 'ར']`)
 - de-duplicate the generated entries and the content of `parsed_verbs.txt` and `particles.txt`
 - write the sorted entries.

##### Output
 - `output/total_lexicon.txt`

##### Issues
 - Applying the particle over the last syllable of some words might generate an ambiguous inflected form. Ex: `སྡེ་པར་` where པར་ can be both the particle and the compressed form of པར་མ་.
