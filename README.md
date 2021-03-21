# search-engine

## Install

Base:

```bash
python -m venv .env
source .env/bin/activate
pip install -U pip setuptools wheel
pip install -U nltk pandas gensim pyzstd
```

(not working) Additional for `zen.py` - Spacy based solution, which is horrendously slow:

```bash
pip install -U spacy[cuda112,transformers,lookups] "dask[complete]"
python -m spacy download en_core_web_trf
```

## Running

Index building mode:

```bash
python main.py
```

Querying after the index was built:

```bash
python query.py
```

## Ideas

- filter stop words
- word proximity metrics
- document length preferrence (grow linearly up to 300 words, then static
- single word - as is preferrably
- > 2 stripping endings is a must
- < 4 order heavily matters
- synonyms dictionary lookup
- identify word priority from the given (ordered list/some nn?)
- extend td.idf to manage overuse of the same phrase (anti-fraud)?
- mega token combinations + 9 word search limit vs storing stripped files and using a rolling window
- error correction?
- work => [(self, [100, 400], [art3, art5]), (ing, [200, 808], [art4, art1]), (ed, [100], [art1]), [(reference to "man", 500), (reference to "job", 550)]] ordered list in terms of relevance to the current query (the best is the word itself, then root, then links (for 2+ words consider links first)). Store reference to self. Issue: how to perform faster lookups of many next words.
