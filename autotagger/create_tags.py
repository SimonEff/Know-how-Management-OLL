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
        parts = []
        try:
            if path.suffix == '.docx':
                doc = docx.Document(str(path))
                for i, para in enumerate(doc.paragraphs):
                    part = para.text
                    parts.append(part)
                    yield path, f"Abschnitt {i+1}, {path.name}", part
            elif path.suffix == '.pdf':
                with path.open("rb") as fp:
                    pdf = PyPDF2.PdfReader(fp)
                    for i, page in enumerate(pdf.pages):
                        part = page.extract_text()
                        parts.append(part)
                        yield path, f"Seite {i+1}, {path.name}", part
        except:
            pass
        if parts:
            yield path, path.name, '\n\n'.join(parts)

def create_tags(text):
    nlp_doc = NLP(text)
    noun_phrases = set(ent.text for ent in nlp_doc.noun_chunks)
    named_entities = set(ent.text for ent in nlp_doc.ents)
    tags = list(noun_phrases | named_entities)
    return {'text': text, 'tags': tags}

print("Create tags...")
data = {name: create_tags(text) for path, name, text in tqdm.tqdm(iter_texts(), unit=" documents")}
pathlib.Path("data.json").write_text(json.dumps(data), encoding='utf-8')
