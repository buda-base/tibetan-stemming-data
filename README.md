# tib_test_data
Data for testing the Tibetan Lucene analyzers

test.txt contains the beginning  of a sutra split in words, the words categorised according to their syllable type:
- nothing added if the syllable can't host any affixed particle,
- /A added if the particle can host an affixed particle and requires a final འ to be valid,
- /B added if the particle can host an affixed particle but doesn't require a འ.