from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse


from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

import os
import csv
import pandas as pd

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


# displays data on a person based on their records from the TEI csv data
@app.get("/people/{unique_key}")
def person_info(request: Request, unique_key: str):
    csv_file = csv.reader(open('TEI CSV Files/TEI people, places, orgs - People.csv', "r"), delimiter=",")

    # getting the headers
    data = pd.read_csv('TEI CSV Files/TEI people, places, orgs - People.csv',nrows=1)
    headers = list(data.columns)

    for row in csv_file:
        if row[1] == unique_key:
            dict = {}
            for i in range(len(headers)):
                dict[headers[i]] = row[i]
    list_of_dict = [dict] # TODO add exception?
    return templates.TemplateResponse('person.html', {'request': request, 'list_of_dict': list_of_dict})
# TODO jpeir1 results in internal server error, seen in tei_xml_files/swarthmore/SW_JC1796.xml, probably misspelled jpier1?

# displays data on a place based on their records from the TEI csv data
@app.get("/places/{unique_key}")
def place_info(request: Request, unique_key: str):
    csv_file = csv.reader(open('TEI CSV Files/TEI people, places, orgs - Places.csv', "r"), delimiter=",")

    # getting the headers
    data = pd.read_csv('TEI CSV Files/TEI people, places, orgs - Places.csv',nrows=1)
    headers = list(data.columns)

    for row in csv_file:
        if row[0] == unique_key:
            dict = {}
            for i in range(len(headers)-3):
                dict[headers[i]] = row[i]
    list_of_dict = [dict] # TODO add exception?
    return templates.TemplateResponse('place.html', {'request': request, 'list_of_dict': list_of_dict})

# displays data on a organization based on their records from the TEI csv data
@app.get("/organizations/{unique_key}")
def organization_info(request: Request, unique_key: str):
    csv_file = csv.reader(open('TEI CSV Files/TEI people, places, orgs - Organizations.csv', "r"), delimiter=",")

    # getting the headers
    data = pd.read_csv('TEI CSV Files/TEI people, places, orgs - Organizations.csv', nrows=1)
    headers = list(data.columns)

    for row in csv_file:
        if row[1] == unique_key:
            dict = {}
            for i in range(len(headers)):
                dict[headers[i]] = row[i]
    list_of_dict = [dict]  # TODO add exception?
    return templates.TemplateResponse('organization.html', {'request': request, 'list_of_dict': list_of_dict})


# displays the raw tei XML documents
@app.get("/xml_test")
def xml_to_html(request: Request):
    # return templates.TemplateResponse('hv_allinsonw_diary_1809_v1.xml',{"request": request})
    return templates.TemplateResponse('test.xml',{"request": request})

@app.get('/linked_test')
def linked_test(request: Request):
    return templates.TemplateResponse('linked_SW_SH1799.html', {'request': request})


@app.get('/linked_manuscripts_test')
def linked_manuscripts_test(request: Request):
    hc_manuscript_list = []

    for filename in os.listdir('Text Files/Haverford Text Files'):
        hc_manuscript_list.append(filename)

    sw_manuscript_list = []

    for filename in os.listdir('Text Files/Swarthmore Text Files'):
        sw_manuscript_list.append(filename)

    return templates.TemplateResponse('linked_homepage.html',{"request": request, "hc_manuscript_list": hc_manuscript_list, "sw_manuscript_list": sw_manuscript_list})


# displays the text file of a linked Haverford manuscript
@app.get("/linked_hc_manuscript/{number}")
def get_hc_manuscript(request: Request, number: int):
    hc_manuscript_list = []

    for filename in os.listdir('templates/Linked HTML Files/Haverford'):
        path = 'Linked HTML Files/Haverford/' + filename
        hc_manuscript_list.append(path)
    source = hc_manuscript_list[number]
    title = source.split('/')[1]
    return templates.TemplateResponse(path, {'request': request})

# displays the text file of a linked Swarthmore manuscript
@app.get("/linked_sw_manuscript/{number}")
def get_sw_manuscript(request: Request, number: int):
    sw_manuscript_list = []

    for filename in os.listdir('templates/Linked HTML Files/Swarthmore'):
        path = 'Linked HTML Files/Swarthmore/' + filename
        sw_manuscript_list.append(path)
    source = sw_manuscript_list[number]
    title = source.split('/')[1]
    return templates.TemplateResponse(path, {'request': request})
