from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse


from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

import os

app = FastAPI()


@app.get("/")
async def root(request: Request):
    hc_manuscript_list = []

    for filename in os.listdir('Text Files/Haverford Text Files'):
        hc_manuscript_list.append(filename)

    sw_manuscript_list = []

    for filename in os.listdir('Text Files/Swarthmore Text Files'):
        sw_manuscript_list.append(filename)


    return templates.TemplateResponse('homepage.html',{"request": request, "hc_manuscript_list": hc_manuscript_list, "sw_manuscript_list": sw_manuscript_list})


# displays the raw tei XML documents
@app.get("/xml_test")
def xml_to_html(request: Request):
    return templates.TemplateResponse('hv_allinsonw_diary_1809_v1.xml',{"request": request})

@app.get("/txt_test")
def txt_to_html(request: Request):
    #source = 'Haverford Text Files/A series of letters written on a Journey to the Oneida, Onondago, and Cayuga Tribes of the Five Nations, by Joseph Sansom: Electronic Version'
    source = 'Swarthmore Text Files/A Brief Account of the Proceedings of the Committee Appointed by the Yearly Meeting of Friends, Held in Baltimore for Promoting the Improvement and Civilization of the Indian Natives: Electronic Version'
    infile = open(source, "r")
    text = infile.read()
    return templates.TemplateResponse('base.html',{'request': request, 'text': text})

@app.get("/hc_manuscript/{number}")
def get_hc_manuscript(request: Request, number: int):
    hc_manuscript_list = []

    for filename in os.listdir('Text Files/Haverford Text Files'):
        path = 'Text Files/Haverford Text Files/' + filename
        hc_manuscript_list.append(path)
    print(hc_manuscript_list)
    source = hc_manuscript_list[number]
    title = source.split('/')[1]
    infile = open(source, "r")
    text = infile.read()
    return templates.TemplateResponse('base.html', {'request': request, 'text': text, 'title': title})

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