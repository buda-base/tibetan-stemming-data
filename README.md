# Data for testing the Tibetan Lucene analyzers

## Generated resources

##### `output/heritage_forms_total.txt`
A general purpose Sanskrit word-list.
Each line is formatted as follows: `inflected<space>operation`

`operation` (to reconstruct the lemma) can have the following values:
  - `\lemma`: the lemma is inserted when more than the operations below are required to find it from the inflected form 
  - `\=`: the inflected form and the lemma are identical
  - `\>NUM`: remove NUM characters at the end of the inflected form
  - `\<NUM`: remove NUM characters at the beginning of the inflected form
  - `\<NUMa>NUMb`: remove NUMa characters at the beginning and NUMb characters at the end of the inflected form

##### Test-set

###### minimal
 - `test_sentence.txt`: 
 - `test_vocab.txt`: 

###### kautalyarthasastra


## `parse_Heritage_XML.py`

##### Input
 - `input/Heritage_XML/`: The XML files copied from [Heritage Resources](https://gitlab.inria.fr/huet/Heritage_Resources)
 - `input/heritage_ambiguous_stems_corrected.csv`: A renamed copy of `output/heritage_ambiguous_stems.csv` that allows for manually deciding which occurence of the stem-string is the actual stem. To fill in the `Start idx` and `End idx` columns, find the indices counting from 1 for the first letter of the inflected form.

##### Action
 - for every XML file:
    - extracts all the form-stem pairs
    - generate the operation string described above
    - prepend `\` before each stem and join all possible stems (ex: "Amayatas \>2\>3\am")

##### Output
 - `output/heritage_forms_total.txt`
 - `output/heritage_ambiguous_forms.txt`: all the ambiguous forms extracted from `heritage_forms_total.txt`
 - `output/heritage_ambiguous_stems.txt`: the forms that could not be processed automatically (see Issues)
 - `log.txt`: figures produced while parsing the XML files.

##### Issues
 - `input/heritage_ambiguous_stems_corrected.csv`: These forms contain more than one time the stem. Someone knowledgeable needs to manually process it. See Input section.
 