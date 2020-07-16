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
import slugify

from bs4 import BeautifulSoup
import re

import json

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# run using: uvicorn main:app --reload

# creates the main page of the app, which shows a list of all the manuscripts
# links are by a for loop in the homepage.html template
@app.get("/")
async def root(request: Request):
    hc_manuscript_list = []

    for filename in os.listdir('Text_Files/Haverford_Text_Files'):
        hc_manuscript_list.append(filename)

    sw_manuscript_list = []

    for filename in os.listdir('Text_Files/Swarthmore_Text_Files'):
        sw_manuscript_list.append(filename)

    return templates.TemplateResponse('homepage.html',{"request": request, "hc_manuscript_list": hc_manuscript_list, "sw_manuscript_list": sw_manuscript_list})


# displays the text file of a Haverford manuscript
@app.get("/hc_manuscript/{number}")
def get_hc_manuscript(request: Request, number: int):
    hc_manuscript_list = []

    for filename in os.listdir('Text_Files/Haverford_Text_Files'):
        path = 'Text_Files/Haverford_Text_Files/' + filename
        hc_manuscript_list.append(path)
    source = hc_manuscript_list[number]
    title = source.split('/')[2]
    slugified_title = 'Haverford/' + slugify.slugify(title)
    infile = open(source, "r")
    text = infile.read()
    return templates.TemplateResponse('base.html', {'request': request, 'text': text, 'title': title, 'slugified_title': slugified_title})


# displays the text file of a Swarthmore manuscript
@app.get("/sw_manuscript/{number}")
def get_sw_manuscript(request: Request, number: int):
    sw_manuscript_list = []

    for filename in os.listdir('Text_Files/Swarthmore_Text_Files'):
        path = 'Text_Files/Swarthmore_Text_Files/' + filename
        sw_manuscript_list.append(path)

    source = sw_manuscript_list[number]
    title = source.split('/')[2]
    slugified_title = 'Swarthmore/' + slugify.slugify(title)
    infile = open(source, "r")
    text = infile.read()
    return templates.TemplateResponse('base.html', {'request': request, 'text': text, 'title': title, 'slugified_title': slugified_title})


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

    for filename in os.listdir('Text_Files/Haverford_Text_Files'):
        hc_manuscript_list.append(filename)

    sw_manuscript_list = []

    for filename in os.listdir('Text_Files/Swarthmore_Text_Files'):
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


# @app.get(URL)
# find: text that matches with 'SW_SH1799_Page_01'
# return the image 'SW_SH1799_Page_01'
# fill in html template with text and image
#
# list of each page name/ image file name
@app.get('/text_and_image_test_home/')
def text_and_image_test_home(request: Request):

    soup = BeautifulSoup(open('Random/SW_JC1797_TEST.xml'), 'lxml')
    #soup = BeautifulSoup(open('Random/linked_hv_allinsonw_diary_1809_v1.xml'), 'lxml')

    for tag in soup.find_all():
        if tag.name == 'persname':
            tag.unwrap()
        elif tag.name == 'placename':
            if tag.string == 'checkPlace':
                tag.decompose()
            else:
                tag.unwrap()
        elif tag.name == 'orgName':
            tag.unwrap()
            # if id != None:
            #     tag.contents.append('{' + id + '}')
            # TODO add id's for links

    s = ''

    # add breaks
    for tag in soup.find_all('pb'):
        page_name = tag.get('facs')
        print(page_name)
        tag.string = '{BREAK}' + page_name + '{TEXT}:'

    document = soup.find('text')

    pages_list = (str(document)).split('{BREAK}')

    x = str(document)

    x = x.replace('<lb></lb>', '\n')
    #TODO try <br>
    x = x.replace('&amp', '&')

    clean = re.sub('<[^>]+>', '', x)

    z = (clean.split('{BREAK}'))

    for i in range(len(z)):
        formatted_page = re.sub("\s+", ' ', z[i])
        z[i] = formatted_page

    pages_dict = {}
    for i in range(len(z)):
        try:
            list_to_dict = (z[i].split('{TEXT}:'))
            pages_dict[list_to_dict[0]] = list_to_dict[1]
        except:
            print(z[i])


    data = []
    page_names_list = []

    for i in pages_dict:
        page_names_list.append(i)
        data.append(pages_dict[i])


    print(page_names_list)



    return templates.TemplateResponse('text_and_image_home_test.html',{'request': request, 'data': data, 'page_names_list': page_names_list})

# test function for handling a paginated manuscript with static files for text and images
# @app.get('/full_manuscript/{page_name}')
# def full_manuscript(request: Request, page_name: str):
#     #need to generate list of page names
#
#     path = 'Pages Test/' + page_name
#     title = page_name
#     f = open('templates/'+path, "r")
#     text = f.read()
#
#    return templates.TemplateResponse('text_and_image_pageview_test.html',{'request': request, 'text': text, 'title': title, 'page_name': page_name})

@app.get('/paginated_manuscripts')
def paginated_manuscripts(request: Request):



# same as above function but doesn't use templates, generates the text for each URL
@app.get('/full_manuscript/{page_name_input}')
def full_manuscript(request: Request, page_name_input: str):

    # 01 page format tests
    #soup = BeautifulSoup(open('Random/SW_JC1797_TEST.xml'), 'lxml')
    #soup = BeautifulSoup(open('templates/Linked XML Files/Swarthmore/linked_SW_Letters_1801_10a.xml'), 'lxml')

    # 001 page format tests
    #soup = BeautifulSoup(open('templates/Linked XML Files/Swarthmore/linked_SW_1791_06_02.xml'), 'lxml')

    #soup = BeautifulSoup(open('templates/Linked XML Files/Swarthmore/linked_SW_JG_1808.xml'), 'lxml')

    # TODO FIX NEXT/PREV JS FOR 100+ PAGE DOCS
    soup = BeautifulSoup(open('templates/Linked XML Files/Swarthmore/linked_SW_JP1796.xml'), 'lxml')
            # KEY ERROR: KeyError: 'SW_JP1796_162'

    for tag in soup.find_all():
        if tag.name == 'persname':
            tag.unwrap()
        elif tag.name == 'placename':
            if tag.string == 'checkPlace':
                tag.decompose()
            else:
                tag.unwrap()
        elif tag.name == 'orgName':
            tag.unwrap()
            # if id != None:
            #     tag.contents.append('{' + id + '}')
            # TODO add id's for links

    s = ''

    # add breaks
    for tag in soup.find_all('pb'):
        try:
            page_name = tag.get('facs')
            tag.string = '{BREAK}' + page_name + '{TEXT}:'
        except:
            pass

    document = soup.find('text')

    pages_list = (str(document)).split('{BREAK}')

    x = str(document)

    x = x.replace('<lb></lb>', '\n')
    #TODO try <br>
    x = x.replace('&amp', '&')

    clean = re.sub('<[^>]+>', '', x)

    z = (clean.split('{BREAK}'))

    for i in range(len(z)):
        formatted_page = re.sub("\s+", ' ', z[i])
        z[i] = formatted_page

    pages_dict = {}
    for i in range(len(z)):
        try:
            list_to_dict = (z[i].split('{TEXT}:'))
            pages_dict[list_to_dict[0]] = list_to_dict[1]
        except:
            print(z[i])


    data = []
    page_names_list = []
    for i in pages_dict:
        page_names_list.append(i)
        data.append(pages_dict[i])

    final_page = page_names_list[-1]
    try:
        text = (pages_dict[page_name_input])
    except:
        return 'Page not found' #TODO IMPROVE THIS maybe wrap the whole thing in try/except block?

    title = page_name_input

    digits = final_page.split('_')[-1]

    num_page_digits = len(digits)



    return templates.TemplateResponse('text_and_image_pageview_test.html',{'request': request, 'text': text, 'title': title,
                                                                           'page_name': page_name_input, 'final_page': final_page, 'num_page_digits': num_page_digits})