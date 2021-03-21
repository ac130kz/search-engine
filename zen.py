from util import save_index
import numpy as np
import dask.dataframe as dd
import string
import spacy
import transformers
import tqdm
import re
import logging
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import EnglishStemmer
logger = logging.getLogger("spacy")
logger.setLevel(logging.ERROR)

nltk.download("punkt")
lemmatizer = WordNetLemmatizer()
stemmer = EnglishStemmer()

# inspired by
# https://prrao87.github.io/blog/spacy/nlp/performance/2020/05/02/spacy-multiprocess.html
pattern = re.compile(r"[A-Za-z0-9\-]{3,25}")
nlp = spacy.load("en_core_web_trf",
                 disable=["parser", "ner", "tagger", "attribute_ruler"])
# nlp.add_pipe("sentencizer")
stopwords = nlp.Defaults.stop_words
summarizer = transformers.pipeline("summarization")


def load_data_blocks(huge=False) -> dd.DataFrame:
    data_blocks = dd.read_csv("all-the-news-2-1.csv" if huge else "articles*.csv",
                              blocksize="8MB",
                              encoding="utf-8", usecols=["id", "title", "date", "content"])
    return data_blocks


def spec_filter(df: dd.DataFrame):
    # properly assigning date format
    df["date"] = dd.to_datetime(df["date"], format="%Y-%m-%d")
    print("Passed dates!")

    # general filtering
    df["clean"] = df["content"].str.findall(pattern).str.join(" ")
    print("Passed general!")

    # pipelining filtering out stopwords
    # df["clean"] = [str(tok.lemma_).lower() for doc in nlp.pipe(df["clean"], batch_size=30) for tok in doc
    #                if tok.is_alpha and tok.text.lower() not in stopwords]

    df["clean"] = df["clean"].map(nltk.word_tokenize)
    print(df["clean"].compute())

    df["clean"] = list(filter(lambda word: word.isalnum(), df["clean"])).map(
        lambda text: text.lower()).filter(lambda word: word not in stopwords).map(lemmatizer.lemmatize).map(stemmer.stem)
    print(df["clean"].compute())
    print("Passed nlp!")

    df["summary"] = summarizer(df["clean"],
                               min_length=10,
                               max_length=100,
                               do_sample=False)
    print("Passed summary!")
    # df["title_tok"]
    # df["title_tag"]
    # df["content_tok"]
    # df["content_tag"]

    return df


def filter_data_blocks(data_blocks: dd.DataFrame) -> dd.DataFrame:

    for i in tqdm.tqdm(range(data_blocks.npartitions)):
        # gets new chunk of data
        df = data_blocks.get_partition(i)

        # persist in RAM for processing
        df = df.persist()

        # assign, run computation, computations require compute
        df = spec_filter(df).compute()

    return data_blocks


if __name__ == "__main__":
    raw_data_blocks = load_data_blocks()

    print(raw_data_blocks)
    # save_index(raw_data_blocks.compute())

    clean_data = filter_data_blocks(raw_data_blocks)
    save_index(clean_data)
