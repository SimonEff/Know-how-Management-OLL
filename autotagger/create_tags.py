import json
import pathlib
import docx
import PyPDF2
import spacy
import tqdm

NLP = spacy.load("de_core_news_lg")
DATA_DIR = pathlib.Path(r"../data/unclean")

def iter_texts(data_dir=DATA_DIR):
    for path in data_dir.glob("**/*.*"):
        try:
            if path.suffix == '.docx':
                doc = docx.Document(str(path))
                text = '\n\n'.join(para.text for para in doc.paragraphs)
                yield path, text
            elif path.suffix == '.pdf':
                with path.open("rb") as fp:
                    pdf = PyPDF2.PdfReader(fp)
                    text = '\n\n'.join(page.extract_text() for page in pdf.pages)
                    yield path, text
        except:
            pass

def create_tags(text):
    nlp_doc = NLP(text)
    noun_phrases = set(ent.text for ent in nlp_doc.noun_chunks)
    named_entities = set(ent.text for ent in nlp_doc.ents)
    tags = list(noun_phrases | named_entities)
    return {'text': text, 'tags': tags}

print("Create tags...")
data = {path.name: create_tags(text) for path, text in tqdm.tqdm(iter_texts(), unit=" documents")}
pathlib.Path("data.json").write_text(json.dumps(data), encoding='utf-8')
