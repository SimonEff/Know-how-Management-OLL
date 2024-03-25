# Know how Management OLL autotagger
## About
* Local tagging using Spacy language model `de-core-news-lg`
* Local search using BM25Okapi
* Web UI using FastAPI & Uvicorn
* PDF support via PyPDF2
* Docx support via python-docx

## Requirements
* Python 3.12
* `python -m pip install -r requirements.txt`

## Usage
* Preprocess documents: `python create_tags.py`
* Run web UI: `python app.py`