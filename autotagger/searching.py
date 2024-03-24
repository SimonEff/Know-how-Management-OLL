import pathlib
import json
import sys
import textwrap

import numpy
from rank_bm25 import BM25Okapi

MAXN = 10
MINSCORE = 0.1

DATA = json.loads(pathlib.Path("data.json").read_text(encoding="utf-8"))

def clean_tags(tags):
    return [tag.strip().lower() for tag in tags]

def find_top_documents(query, maxn=MAXN, minscore=MINSCORE):
    documents = list(DATA.items())
    scorer = BM25Okapi([clean_tags(doc['tags']) for filename, doc in documents])
    scores = scorer.get_scores(query)
    top_docs = numpy.argsort(scores)[::-1][:MAXN]
    for i in top_docs:
        filename, doc = documents[i]
        score = scores[i]
        if score < MINSCORE:
            break
        yield {
            'filename': filename,
            'excerpt': textwrap.shorten(doc['text'], 100),
            'tags': doc['tags'],
            'score': int(100*score),
        }

if __name__ == '__main__':
    query = clean_tags(sys.argv[1:])
    for match in find_top_documents(query):
        print(f"{match['filename']} (Score: {match['score']})")
