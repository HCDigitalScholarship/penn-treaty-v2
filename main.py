from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse


from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

import os

app = FastAPI()

# run using: uvicorn main:app --reload

# creates the main page of the app, which shows a list of all the manuscripts
# links are by a for loop in the homepage.html template
@app.get("/")
async def root(request: Request):
    hc_manuscript_list = []

    for filename in os.listdir('Text Files/Haverford Text Files'):
        hc_manuscript_list.append(filename)

    sw_manuscript_list = []

    for filename in os.listdir('Text Files/Swarthmore Text Files'):
        sw_manuscript_list.append(filename)

    return templates.TemplateResponse('homepage.html',{"request": request, "hc_manuscript_list": hc_manuscript_list, "sw_manuscript_list": sw_manuscript_list})


# displays the text file of a Haverford manuscript
@app.get("/hc_manuscript/{number}")
def get_hc_manuscript(request: Request, number: int):
    hc_manuscript_list = []

    for filename in os.listdir('Text Files/Haverford Text Files'):
        path = 'Text Files/Haverford Text Files/' + filename
        hc_manuscript_list.append(path)
    source = hc_manuscript_list[number]
    title = source.split('/')[1]
    infile = open(source, "r")
    text = infile.read()
    return templates.TemplateResponse('base.html', {'request': request, 'text': text, 'title': title})


# displays the text file of a Swarthmore manuscript
@app.get("/sw_manuscript/{number}")
def get_sw_manuscript(request: Request, number: int):
    sw_manuscript_list = []

    for filename in os.listdir('Text Files/Swarthmore Text Files'):
        path = 'Text Files/Swarthmore Text Files/' + filename
        sw_manuscript_list.append(path)

    source = sw_manuscript_list[number]
    title = source.split('/')[1]
    infile = open(source, "r")
    text = infile.read()
    return templates.TemplateResponse('base.html', {'request': request, 'text': text, 'title': title})