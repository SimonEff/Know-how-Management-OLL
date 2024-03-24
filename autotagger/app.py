import pathlib
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import searching

app = FastAPI()
BASE_DIR = pathlib.Path(__file__).parent
templates = Jinja2Templates(directory=[BASE_DIR / "templates"])
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/', response_class=HTMLResponse)
async def index(request: Request, query: str | None = None):
    results = []
    if query is not None:
        query_words = searching.clean_tags(query.split())
        results = list(searching.find_top_documents(query_words))
    return templates.TemplateResponse("index.html", {
        "request": request,
        "results": results,
        "query": query or '',
    })

if __name__ == "__main__":
    import uvicorn
    import webbrowser
    webbrowser.open('http://127.0.0.1:8000')
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
