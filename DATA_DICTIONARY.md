# Data Dictionary

## `sample_sentences.csv`
- `sentence`: artificial example sentence.
- `target_word`: ambiguous word the system should disambiguate.
- `reference_sense`: expected sense label used for evaluation.

## `sense_inventory.csv`
- `word`: ambiguous target word.
- `sense_id`: unique identifier for a word sense.
- `sense_label`: human-readable meaning label.
- `definition`: short gloss for the sense.
- `synonyms`: semicolon-separated synonym-like terms.
- `hypernym`: broader category associated with the sense.
- `related_words`: semicolon-separated context cues used by the WSD algorithm.
