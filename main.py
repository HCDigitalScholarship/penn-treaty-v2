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

@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse('about.html', {'request': request})

@app.get("/bibliography")
async def about(request: Request):
    return templates.TemplateResponse('bibliography.html', {'request': request})

@app.get("/credits")
async def about(request: Request):
    return templates.TemplateResponse('credits.html', {'request': request})

@app.get("/map-gallery")
async def map_gallery(request: Request):
    return templates.TemplateResponse('map_gallery.html', {'request': request})

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse('homepage.html', {'request': request})

@app.get("/overviewmap_traveler")
async def map_traveler(request: Request):
    return templates.TemplateResponse('overviewmap_traveler.html', {'request': request})

@app.get("/overviewmap_date")
async def map_date(request: Request):
    return templates.TemplateResponse('overviewmap_date.html', {'request': request})

@app.get("/overviewmap_popularlocations")
async def map_popularlocations(request: Request):
    return templates.TemplateResponse('overviewmap_popularlocations.html', {'request': request})

# creates the main page of the app, which shows a list of all the manuscripts
# links are by a for loop in the homepage.html template
@app.get("/manuscripts")
async def manuscripts(request: Request):

    # sw_data and hc_data lists created using get_manuscript_data.py in scripts folder

    sw_data = [['Halliday Jackson 1800 Journal (continued)', 'swarthmore/SW_HJ1800.xml/SW_HJ1800_001', 'sw_manuscript/53', 'Journal'],
               ['The Committee Appointed to Confer With the Friends who Attended the Indian Treaty', 'swarthmore/SW_Letters_179-_MM_DD.xml/SW_Letters_179-_MM_DD_Page_1', 'sw_manuscript/47', 'Report'],
               ['A Brief Account of the Proceedings of the Committee Appointed by the Yearly Meeting of Friends, Held in Baltimore for Promoting the Improvement and Civilization of the Indian Natives', 'swarthmore/SW_BYM1806.xml/SW_BYM1806_001', 'sw_manuscript/22', 'Printed Book'],
               ["Jacob Lindley's Account, 1793", 'swarthmore/SW_JL1793.xml/SW_JL1793_Page_049', 'sw_manuscript/46', 'Printed Journal'],
               ['Jonathan Thomas His Book 1798', 'swarthmore/SW_JT1798.xml/SW_JT1798_001', 'sw_manuscript/23', 'Journal'],
               ['Account of Canandaigua Treaty Negotiations', 'swarthmore/SW_Letters_1794_12_20.xml/SW_Letters_1794_12_20_Page_1', 'sw_manuscript/51', 'Letters'],
               ['Subscriptions from Shrewsbury Monthly Meeting for Promoting the Civilization and Well-Being of the Indian Natives', 'swarthmore/SW_NYYM_Subscriptions.xml/SW_NYYMsubscriptions_Page_001', 'sw_manuscript/27', ''],
               ["Halliday Jackson's Journal, 1806", 'swarthmore/SW_HJ1806.xml/SW_HJ1806_Page_001', 'sw_manuscript/20', 'Journal'],
               ['Letter to the Cherokee Nation from Philadelphia Yearly Meeting', 'swarthmore/SW_Letters_1792_02_19.xml/SW_Letters_1792_02_19_Page_1', 'sw_manuscript/1', 'Letters'],
               ['John Peirce Notes, on a visit to Several Tribes of Indians, 1796', 'swarthmore/SW_JP1796.xml/SW_JP1796_001', 'sw_manuscript/29', 'Diaries'],
               ['Account of the Exercise and Experience of an Indian Man', 'swarthmore/SW_NYYM_Man.xml/SW_NYYM_Man_Page_001', 'sw_manuscript/44', 'Manuscript'],
               ['Letter from Cornplanter to Quakers', 'swarthmore/SW_Letters_1791_02_10.xml/SW_Letters_1791_02_10_Page_1', 'sw_manuscript/33', 'Letters'], ['Letter to John Parrish & others from Gen. McKee', 'swarthmore/SW_Letters_1793_08_26.xml/SW_Letters_1793_08_26_001', 'sw_manuscript/6', 'Letters'],
               ['Baltimore Yearly Meeting Indian Committee Minutes, 1795-1815', 'swarthmore/SW_BYM_minutes.xml/BYM_Page_001', 'sw_manuscript/38', 'Minute Books'], ['Letter to John Drinker from John Parrish et. al.', 'swarthmore/SW_Letters_1793_08_24.xml/SW_Letters_1793_08_24_Page_1', 'sw_manuscript/12', 'Letters'],
               ['Reports of the Indian Committee to New York Yearly Meeting, 1795-1806', 'swarthmore/SW_NYYM_reports.xml/SW_NYYM_reports_Page_001', 'sw_manuscript/2', 'Minute Books'],
               ['Letter to Western Indians from the Meeting for Sufferings', 'swarthmore/SW_Letters_1793_04_19.xml/SW_Letters_1793_04_19_Page_1', 'sw_manuscript/24', 'Letters'],
               ["Joseph Moore's Journal", None, 'sw_manuscript/18', 'Printed Journal'],
               ['Notes of a Journey taken by Elisha Tyson & James Gillingham on a Visit to some Indians in the neighbourhood of Fort Wayne', 'swarthmore/SW_JG_1808.xml/SW_JG_1808_001', 'sw_manuscript/0', 'Diaries'],
               ['The Committee appointed in the 5 mo 1795', 'swarthmore/SW_1796_12_15.xml/SW_1796_12_15_001', 'sw_manuscript/48', ''],
               ['Letter from Henry Simmons to Israel Chapin', 'swarthmore/SW_SH1799.xml/SW_SH1799_Page_01', 'sw_manuscript/30', 'Letters'],
               ["Wm. Hartshorne's Journal of Journey to Detroit 1793", 'swarthmore/SW_WH1793.xml/SW_WH1793_Page_01', 'sw_manuscript/43', 'Diaries'],
               ['Travels in Some Parts of North America, in the Years 1804, 1805, & 1806, by Robert Sutcliff', 'swarthmore/SW_Sutcliff.xml/SW_Sutcliff_Page_iii', 'sw_manuscript/28', 'Diaries'],
               ["Missionary's address to the chiefs of the six nation Indian & Their answers", 'swarthmore/SW_1805_00_00.xml/SW_1805_00_00_Page_1', 'sw_manuscript/31', 'Manuscript'],
               ['Copy of a manuscript respecting the American Indians (A)', 'swarthmore/SW_Letters_1801_10a.xml/SW_Letters_1801_10a_Page_01', 'sw_manuscript/16', 'Manuscript'],
               ['Letter from Quakers to Cornplanter', 'swarthmore/SW_1791_06_02.xml/SW_1791_06_02_001', 'sw_manuscript/42', 'Letters'],
               ['Some Account of Rachel Coope (Journal B)', 'swarthmore/SW_RC1805b.xml/SW_RC1805b_Page_01', 'sw_manuscript/15', 'Diaries'],
               ["Joshua Sharpless' Journal [Visit to Upper Canada and Parts Adjacent], 1797", 'swarthmore/SW_JS1797.xml/SW_JS1797_Page_01', 'sw_manuscript/50', 'Diaries'],
               ['Letter to the Indians Assembled at the Rapids of the Miami', 'swarthmore/SW_Letters_1793_07_17.xml/SW_Letters_1793_07_17_Page_1', 'sw_manuscript/45', 'Letters'],
               ['Some Account of Rachel Coope (Journal A)', 'swarthmore/SW_RC1805a.xml/SW_RC1805a_Page_01', 'sw_manuscript/40', 'Diaries'],
               ['Journal of a Visit to the Seneca Indians, 1796, by James Cooper of Woodbury, N.J.', 'swarthmore/SW_JC1796.xml/SW_JC1796_001', 'sw_manuscript/49', 'Diaries'],
               ['Letter from Quakers to General Wayne, 1795', 'swarthmore/SW_Letters_1795_05_25.xml/SW_Letters_1795_05_25_Page_1', 'sw_manuscript/21', 'Letters'],
               ["Joseph Clark's Account of a Journey to the Indian Country, 1797", 'swarthmore/SW_JC1797.xml/SW_JC1797_Page_01', 'sw_manuscript/4', 'Printed Journal'],
               ["Joshua Sharpless's Journal Into Indian Country, 1798", 'swarthmore/SW_JS1798.xml/SW_JS1798_001', 'sw_manuscript/35', 'Diaries'],
               ['A Mission to the Indians from the Indian Committee of Baltimore Yearly Meeting to Fort Wayne, in 1804', 'swarthmore/SW_GH1804.xml/SW_GH1804_001', 'sw_manuscript/39', 'Report'],
               ['Letter to the Shawanese, Delawares & others from Quakers of Pennsylvania and New Jersey, 1795', 'swarthmore/SW_Letters_1795_05_22.xml/SW_Letters_1795_05_22_Page_1', 'sw_manuscript/54', 'Letters'],
               ['Treasury Account of Goods to be sent to the Indians, 1795', 'swarthmore/SW_Letters_1795_05_23.xml/SW_Letters_1795_05_23_Page_1', 'sw_manuscript/26', 'Financial Records'],
               ["Joseph Clark's Of a second Visit to the Indian Country, 1801", 'swarthmore/SW_JC1801.xml/SW_JC1801_Page_1', 'sw_manuscript/14', 'Journal'],
               ['Letters to Elizabeth Townsend', 'swarthmore/SW_Letters_1801_10_15.xml/SW_Letters_1801_10_15_Page_01', 'sw_manuscript/11', 'Letters'],
               ['Letter to the Quarterly Meeting of Friends at Hopewell', 'swarthmore/SW_Letters_1794_00_00.xml/Misc_mss_1794_00_00001', 'sw_manuscript/37', 'Letters'],
               ['Letter to Friends from David Fowler', 'swarthmore/SW_Letters_1793_03_20.xml/SW_Letters_1793_03_20_Page_1', 'sw_manuscript/8', 'Letters'],
               ["Halliday Jackson's Book [of Corrrespondence], Genesinguhta, 1798-1800", 'swarthmore/SW_HJ1798.xml/SW_HJ1798_001', 'sw_manuscript/5', 'Letter Books'],
               ['New York Yearly Meeting Committee on Indian Concerns Scrapbook', 'swarthmore/SW_NYYM_scrapbook.xml/NYYM_scrapbook_003', 'sw_manuscript/7', 'Scrapbooks'],
               ['The United States to Joseph Johnston', 'swarthmore/SW_1798_06_15.xml/SW_1798_06_15_Page_1', 'sw_manuscript/17', 'Financial Records'],
               ['Some Account of Rachel Coope [edited by Joshua Sharpless]', 'swarthmore/SW_RC1805.xml/SW_RC1805_Page_05', 'sw_manuscript/13', 'Diaries'],
               ['Minutes of the Committee on Indian Concern No 1', 'swarthmore/SW_NYYM_minutes.xml/NYYM_minutes_Page_001', 'sw_manuscript/41', 'Minute Books'],
               ['Extract The Speech of John Skenando principal Chief of the Oneida Nation', 'swarthmore/SW_NYYM_Skenando.xml/SW_NYYM_Skenando_Page_001', 'sw_manuscript/9', 'Speeches'],
               ['Isaac Coates Journal of Journeys to the Indian Country', 'swarthmore/SW_IC1799.xml/SW_IC1799_Page_01', 'sw_manuscript/34', 'Printed Journal'],
               ['Invoice of Gifts, 1795', 'swarthmore/SW_Letters_1795_05_25invoice.xml/SW_Letters_1795_05_25invoice_001', 'sw_manuscript/25', 'Financial Records'],
               ['Letter from Tobias Lear to Quakers', 'swarthmore/SW_Letters_1792_02_11.xml/SW_Letters_1792_02_11_Page_1', 'sw_manuscript/10', 'Letters'],
               ['Sketch of the Customs, Religion and Government of the Seneca Indians, in 1800', 'swarthmore/SW_HJ1830.xml/SW_HJ1830_001', 'sw_manuscript/3', 'Book'],
               ['Address to the Six Nations', 'swarthmore/SW_Letters_1794_09_09.xml/SW_Letters_1794_09_09_001', 'sw_manuscript/36', 'Letters'],
               ['Journal of Joshua Evans 1795-1796 (E)', 'swarthmore/SW_JE1796E.xml/SW_JE1796E_Page_01', 'sw_manuscript/52', 'Diaries'],
               ['The Bank of Faith and Works United', 'swarthmore/SW_Ripley.xml/Ripley074', 'sw_manuscript/19', 'Printed Book'],
               ['Life of Thomas Eddy', None, 'sw_manuscript/32', 'Printed Book']]

    hc_data = [['A series of letters written on a Journey to the Oneida, Onondago, and Cayuga Tribes of the Five Nations, by Joseph Sansom', 'haverford/hv_sansomj_letters_1796.xml/hv_sansomj_letters_1796_001', 'hc_manuscript/0', 'Letter Books'],
               ['Joel Swayne Diary', 'haverford/hv_swaynej_diary_1798.xml/hv_swaynej_diary_1798_001', 'hc_manuscript/5', 'Diaries'],
               ['William Allinson Diary, Volume 1', 'haverford/hv_allinsonw_diary_1809_v1.xml/hv_allinsonw_diary_1809_v1_001', 'hc_manuscript/3', 'Diaries'],
               ['William Allinson Diary, Volume 2', 'haverford/hv_allinsonw_diary_1809_v2.xml/hv_allinsonw_diary_1809_v2_001', 'hc_manuscript/2', 'Diaries'],
               ['William Allinson Diary, Volume 3', 'haverford/hv_allinsonw_diary_1809_v3.xml/hv_allinsonw_diary_1809_v3_001', 'hc_manuscript/1', 'Diaries'],
               ['Some Account of our Journey to Cannandaigue', 'haverford/hv_bacond_account_1794.xml/hv_bacond_account_1794_001', 'hc_manuscript/6', 'Diaries'],
               ['Account of I. Coates, J. Sharpless, & J. Pierce, visits to Indian Reservation, NY', 'haverford/hv_coatesi_account_1798.xml/hv_coatesi_account_1798_001', 'hc_manuscript/4', 'Diaries']]



    return templates.TemplateResponse('manuscripts.html',{"request": request, "hc_data": hc_data, "sw_data": sw_data})


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

#TODO NEED TRY/EXCEPT FOR PEOPLE/PLACES/ORGS for when item isn't found
# pyindian is not found in orgs dict (seen in hv_coatesi_account_1798)

# displays data on a person based on their records from the TEI csv data
@app.get("/people/{unique_key}")
def person_info(request: Request, unique_key: str):
    csv_file = csv.reader(open('TEI CSV Files/TEI people, places, orgs - People.csv', "r", encoding="utf8"), delimiter=",")

    # getting the headers
    data = pd.read_csv('TEI CSV Files/TEI people, places, orgs - People.csv',nrows=1)
    headers = list(data.columns)

    # removes underscores from the headers of the csv
    headers = [header.replace('_',' ') for header in headers]

    # finds the correct row in the csv file that matches with the unique_key
    # writes the data from the row into a dictionary
    for row in csv_file:
        if row[1] == unique_key:
            dict = {}
            for i in range(2, len(headers)-4):
                if row[i]:
                    dict[headers[i].capitalize()] = row[i]

    csv_file = csv.reader(open('TEI CSV Files/TEI people, places, orgs - Organizations.csv',  "r", encoding="utf8"),
                          delimiter=",")  # resets the csv file iterator

    # adds links to each item in affiliations
    try:
        item = 'Affiliations'
        affiliations_list = dict[item].split(';')
        # affiliations_list = ['''<a href="/organizations/''' + name + '">' + name + '</a>' for name in affiliations_list]
        for i in range(len(affiliations_list)):
            id = affiliations_list[i]
            name = id
            for row in csv_file:
                if row[1] == id:
                    name = row[3]
                    csv_file = csv.reader(open('TEI CSV Files/TEI people, places, orgs - Organizations.csv', "r", encoding="utf8"), delimiter=",") # resets the csv file iterator
                    break
            affiliations_list[i] = f'<a href="/organizations/{id}">{name}</a>'

        dict[item] = ', '.join(affiliations_list)
    except:
        pass

    csv_file = csv.reader(open('TEI CSV Files/TEI people, places, orgs - Places.csv',  "r", encoding="utf8"),
                        delimiter=",")  # resets the csv file iterator
    
    # adds links to each item in places
    try:
        item1 = 'Birth place'
        item2 = 'Death place'
        id1 = dict[item1]
        id2 = dict[item2]
        name1 = id1
        name2 = id2
        for row in csv_file:
            if row[0] == id1:
                name1 = row[1]
            if row[0] == id2:
                name2 = row[1]
        dict[item1] = f'<a href="/places/{id1}">{name1}</a>'
        dict[item2] = f'<a href="/places/{id2}">{name2}</a>'

    except:
        pass

    # adds a link to the entry lcnaf uri
    try:
        temp = dict['lcnaf uri']
        dict['lcnaf uri'] = f'<a href="{temp}">{temp}</a>'
    except:
        pass

    try:
        del dict['done or not'] # removes unnecessary field
    except:
        pass
    list_of_dict = [dict] # TODO add exception?

    with open('Scripts/people_related_pages.txt') as json_file:
        people_related_pages = json.load(json_file)

    if unique_key in people_related_pages.keys():
        related_pages = people_related_pages[unique_key]
    else:
        related_pages = {0: {'title': 'No related documents found'}}
    
    return templates.TemplateResponse('person.html', {'request': request, 'list_of_dict': list_of_dict, 'related_pages': related_pages})
# TODO jpeir1 results in internal server error, seen in tei_xml_files/swarthmore/SW_JC1796.xml, probably misspelled jpier1?

# displays data on a place based on their records from the TEI csv data
@app.get("/places/{unique_key}")
def place_info(request: Request, unique_key: str):
    csv_file = csv.reader(open('TEI CSV Files/TEI people, places, orgs - Places.csv', "r", encoding="utf8"), delimiter=",")

    # getting the headers
    data = pd.read_csv('TEI CSV Files/TEI people, places, orgs - Places.csv', nrows=1)
    headers = list(data.columns)

    # finds the correct row in the csv file that matches with the unique_key
    # writes the data from the row into a dictionary
    for row in csv_file:
        if row[0] == unique_key:
            dict = {}
            for i in range(len(headers)):
                if row[i]:
                    dict[headers[i].capitalize()] = row[i]

    # removes unnecessary fields
    try:
        del dict['X']
        del dict['Type']
    except:
        pass

    list_of_dict = [dict] # TODO add exception?

    with open('Scripts/places_related_pages.txt') as json_file:
        places_related_pages = json.load(json_file)  
    if unique_key in places_related_pages.keys():
        related_pages = places_related_pages[unique_key]
    else:
        related_pages = {0: {'title': 'No related documents found'}}
    return templates.TemplateResponse('place.html', {'request': request, 'list_of_dict': list_of_dict, 'related_pages': related_pages})

# displays data on a organization based on their records from the TEI csv data
@app.get("/organizations/{unique_key}")
def organization_info(request: Request, unique_key: str):
    csv_file = csv.reader(open('TEI CSV Files/TEI people, places, orgs - Organizations.csv', "r", encoding="utf8"), delimiter=",")

    # getting the headers
    data = pd.read_csv('TEI CSV Files/TEI people, places, orgs - Organizations.csv', nrows=1)
    headers = list(data.columns)

    # removes underscores from the headers of the csv
    headers = [header.replace('_', ' ') for header in headers]

    # finds the correct row in the csv file that matches with the unique_key
    # writes the data from the row into a dictionary
    for row in csv_file:
        if row[1] == unique_key:
            dict = {}
            for i in range(2, len(headers)):
                if row[i]:
                    dict[headers[i].capitalize()] = row[i]

    csv_file = csv.reader(open('TEI CSV Files/TEI people, places, orgs - Organizations.csv', "r", encoding="utf8"), delimiter=",") # resets the csv file iterator

    # adds links to data in the see also category (same as affiliations)
    try:
        item = 'See also'
        affiliations_list = dict[item].split(';')
        # affiliations_list = ['''<a href="/organizations/''' + name + '">' + name + '</a>' for name in affiliations_list]
        for i in range(len(affiliations_list)):
            id = affiliations_list[i]
            name = id
            for row in csv_file:
                if row[1] == id:
                    name = row[3]
                    csv_file = csv.reader(open('TEI CSV Files/TEI people, places, orgs - Organizations.csv', "r", encoding="utf8"), delimiter=",") # resets the csv file iterator
                    break
            affiliations_list[i] = f'<a href="/organizations/{id}">{name}</a>'

        dict[item] = ', '.join(affiliations_list)
    except:
        pass

    # adds a link to the entry lcnaf uri
    try:
        temp = dict['Lcnaf uri']
        dict['Lcnaf uri'] = f'<a href="{temp}">{temp}</a>'
    except:
        pass

    list_of_dict = [dict]  # TODO add exception?

    
    with open('Scripts/org_related_pages.txt') as json_file:
        org_related_pages = json.load(json_file)
    if unique_key in org_related_pages.keys():
        related_pages = org_related_pages[unique_key]
    else:
        related_pages = {0: {'title': 'No related documents found'}}
    return templates.TemplateResponse('organization.html', {'request': request, 'list_of_dict': list_of_dict, 'related_pages': related_pages})

@app.get("/profiles")
async def profiles(request: Request):
    csv_file = csv.reader(open('TEI CSV Files/TEI people, places, orgs - People.csv', "r", encoding="utf8"), delimiter=",")
    next(csv_file)
    people_data = list(csv_file)
    csv_file = csv.reader(open('TEI CSV Files/TEI people, places, orgs - Places.csv', "r", encoding="utf8"), delimiter=",")
    next(csv_file)
    places_data = list(csv_file)
    csv_file = csv.reader(open('TEI CSV Files/TEI people, places, orgs - Organizations.csv', "r", encoding="utf8"), delimiter=",")
    next(csv_file)
    org_data = list(csv_file)

    return templates.TemplateResponse('profiles.html', {'request': request, 'people_data': people_data, 'places_data': places_data, 'org_data': org_data})    

# test home page for displaying linked manuscripts
# generates a list of all links to all manuscripts with linked data
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

# generates a list of all paginated manuscripts
@app.get('/paginated_manuscripts')
def paginated_manuscripts(request: Request):

    # this dictionary can be generated by adapting the get_manuscript_data.py file in the scripts folder
    # first_page_dict is a dictionary of each file name and the corresponding first page
    first_page_dict = {'haverford/hv_sansomj_letters_1796.xml': 'hv_sansomj_letters_1796_001',
     'haverford/hv_swaynej_diary_1798.xml': 'hv_swaynej_diary_1798_001',
     'haverford/hv_allinsonw_diary_1809_v1.xml': 'hv_allinsonw_diary_1809_v1_001',
     'haverford/hv_allinsonw_diary_1809_v2.xml': 'hv_allinsonw_diary_1809_v2_001',
     'haverford/hv_allinsonw_diary_1809_v3.xml': 'hv_allinsonw_diary_1809_v3_001',
     'haverford/hv_bacond_account_1794.xml': 'hv_bacond_account_1794_001',
     'haverford/hv_coatesi_account_1798.xml': 'hv_coatesi_account_1798_001',
     'swarthmore/SW_HJ1800.xml': 'SW_HJ1800_001',
     'swarthmore/SW_Letters_179-_MM_DD.xml': 'SW_Letters_179-_MM_DD_Page_1',
     'swarthmore/SW_BYM1806.xml': 'SW_BYM1806_001', 'swarthmore/SW_JL1793.xml': 'SW_JL1793_Page_049',
     'swarthmore/SW_JT1798.xml': 'SW_JT1798_001',
     'swarthmore/SW_Letters_1794_12_20.xml': 'SW_Letters_1794_12_20_Page_1',
     'swarthmore/SW_NYYM_Subscriptions.xml': 'SW_NYYMsubscriptions_Page_001',
     'swarthmore/SW_HJ1806.xml': 'SW_HJ1806_Page_001',
     'swarthmore/SW_Letters_1792_02_19.xml': 'SW_Letters_1792_02_19_Page_1',
     'swarthmore/SW_JP1796.xml': 'SW_JP1796_001', 'swarthmore/SW_NYYM_Man.xml': 'SW_NYYM_Man_Page_001',
     'swarthmore/SW_Letters_1791_02_10.xml': 'SW_Letters_1791_02_10_Page_1',
     'swarthmore/SW_Letters_1793_08_26.xml': 'SW_Letters_1793_08_26_001',
     'swarthmore/SW_BYM_minutes.xml': 'BYM_Page_001',
     'swarthmore/SW_Letters_1793_08_24.xml': 'SW_Letters_1793_08_24_Page_1',
     'swarthmore/SW_NYYM_reports.xml': 'SW_NYYM_reports_Page_001',
     'swarthmore/SW_Letters_1793_04_19.xml': 'SW_Letters_1793_04_19_Page_1',
     'swarthmore/SW_JG_1808.xml': 'SW_JG_1808_001', 'swarthmore/SW_1796_12_15.xml': 'SW_1796_12_15_001',
     'swarthmore/SW_SH1799.xml': 'SW_SH1799_Page_01', 'swarthmore/SW_WH1793.xml': 'SW_WH1793_Page_01',
     'swarthmore/SW_Sutcliff.xml': 'SW_Sutcliff_Page_iii', 'swarthmore/SW_1805_00_00.xml': 'SW_1805_00_00_Page_1',
     'swarthmore/SW_Letters_1801_10a.xml': 'SW_Letters_1801_10a_Page_01',
     'swarthmore/SW_1791_06_02.xml': 'SW_1791_06_02_001', 'swarthmore/SW_RC1805b.xml': 'SW_RC1805b_Page_01',
     'swarthmore/SW_JS1797.xml': 'SW_JS1797_Page_01',
     'swarthmore/SW_Letters_1793_07_17.xml': 'SW_Letters_1793_07_17_Page_1',
     'swarthmore/SW_RC1805a.xml': 'SW_RC1805a_Page_01', 'swarthmore/SW_JC1796.xml': 'SW_JC1796_001',
     'swarthmore/SW_Letters_1795_05_25.xml': 'SW_Letters_1795_05_25_Page_1',
     'swarthmore/SW_JC1797.xml': 'SW_JC1797_Page_01', 'swarthmore/SW_JS1798.xml': 'SW_JS1798_001',
     'swarthmore/SW_GH1804.xml': 'SW_GH1804_001',
     'swarthmore/SW_Letters_1795_05_22.xml': 'SW_Letters_1795_05_22_Page_1',
     'swarthmore/SW_Letters_1795_05_23.xml': 'SW_Letters_1795_05_23_Page_1',
     'swarthmore/SW_JC1801.xml': 'SW_JC1801_Page_1',
     'swarthmore/SW_Letters_1801_10_15.xml': 'SW_Letters_1801_10_15_Page_01',
     'swarthmore/SW_Letters_1794_00_00.xml': 'Misc_mss_1794_00_00001',
     'swarthmore/SW_Letters_1793_03_20.xml': 'SW_Letters_1793_03_20_Page_1',
     'swarthmore/SW_HJ1798.xml': 'SW_HJ1798_001', 'swarthmore/SW_NYYM_scrapbook.xml': 'NYYM_scrapbook_003',
     'swarthmore/SW_1798_06_15.xml': 'SW_1798_06_15_Page_1', 'swarthmore/SW_RC1805.xml': 'SW_RC1805_Page_05',
     'swarthmore/SW_NYYM_minutes.xml': 'NYYM_minutes_Page_001',
     'swarthmore/SW_NYYM_Skenando.xml': 'SW_NYYM_Skenando_Page_001', 'swarthmore/SW_IC1799.xml': 'SW_IC1799_Page_01',
     'swarthmore/SW_Letters_1795_05_25invoice.xml': 'SW_Letters_1795_05_25invoice_001',
     'swarthmore/SW_Letters_1792_02_11.xml': 'SW_Letters_1792_02_11_Page_1',
     'swarthmore/SW_HJ1830.xml': 'SW_HJ1830_001', 'swarthmore/SW_Letters_1794_09_09.xml': 'SW_Letters_1794_09_09_001',
     'swarthmore/SW_JE1796E.xml': 'SW_JE1796E_Page_01', 'swarthmore/SW_Ripley.xml': 'Ripley074'}

    return templates.TemplateResponse('paginated_manuscripts_home.html',{'request': request, 'first_page_dict': first_page_dict})

# same as above function but doesn't use templates, generates the text for each URL
# creates paginated manuscripts with linked data
@app.get('/full_manuscript/{hc_or_swat}/{manuscript_name}/{page_name_input}')
def full_manuscript(request: Request, manuscript_name: str, page_name_input: str, hc_or_swat: str):

    #soup = BeautifulSoup(open('templates/Linked XML Files/Swarthmore/linked_SW_JP1796.xml'), 'lxml')
            # KEY ERROR: KeyError: 'SW_JP1796_162'

    # creates the path to the manuscript file
    manuscript_name = hc_or_swat +'/' + manuscript_name
    path = f'templates/tei_xml_files/{manuscript_name}'

    # uses beautifulsoup to parse the raw xml file
    soup = BeautifulSoup(open(path, encoding="utf8"), 'lxml')

    # gets the title of the page
    title = soup.find('title')
    title = title.string.split(':')[0]
    # contents = re.sub('  +', '', contents)
    title = re.sub("\s+", ' ', title)



    # removes all the xml line break tags to make parsing easier
    for tag in soup.find_all('lb'):
        tag.decompose()

    # loop through all tags and replace persname, placename, and orgname with links to the data they represent
    for tag in soup.find_all():
        if tag.name == 'persname':
            # gets the unique id for the person
            id = tag.get('key')
            try:
                if id is not None:
                    # saves the contents of the tag temporarily, then replaces the tag contents with an html link element
                    temp_tag_contents = tag.string
                    if temp_tag_contents == None:
                        tag.string = tag.contents.join('')
                    tag.string = f'<a href="/people/{id}">{temp_tag_contents}</a>'
                tag.unwrap()
            except:
                print(tag)
        elif tag.name == 'placename':
            # gets rid of checkPlace tags, which do not have a key in the xml
            if tag.string == 'checkPlace':
                tag.decompose()
            else:
                # gets the unique id for the place
                id = tag.get('key')
                try:
                    if id is not None:
                        # saves the contents of the tag temporarily, then replaces the tag contents with an html link element
                        temp_tag_contents = tag.string
                        if temp_tag_contents == None:
                            tag.string = tag.contents.join('')
                        tag.string = f'<a href="/places/{id}">{temp_tag_contents}</a>'
                    tag.unwrap()
                except:
                    print(tag)
        elif tag.name == 'orgname':
            # gets the unique id for the organization
            id = tag.get('key')
            try:
                # saves the contents of the tag temporarily, then replaces the tag contents with an html link element
                if id is not None:
                    temp_tag_contents = tag.string
                    if temp_tag_contents == None:
                        tag.string = tag.contents.join('')
                    tag.string = f'<a href="/organizations/{id}">{temp_tag_contents}</a>'
                tag.unwrap()
            except:
                print(tag)
                  

    # inserts a string at each page break xml tag to be used to split up the xml file by page lat31
    # page names are later used as keys in the dictionary of all the pages as strings
    for tag in soup.find_all('pb'):
        page_name = tag.get('facs')
        print(page_name)
        if page_name:
            tag.string = '{BREAK}' + page_name + '{TEXT}:'

    # grabs the text section of the xml file
    document = soup.find('text')

    # casts the xml tree to a string
    # cleans up the string created from the xml
    x = str(document)
    x = x.replace('<lb></lb>', '\n')
    x = x.replace('&amp', '&')

    # cleans up encoding problems and gets rid of anything between < and >
    clean = re.sub('<[^>]+>', '', x)
    clean = clean.replace('&lt;', '<')
    clean = clean.replace('&gt;', '>')

    # splits the string by page into a list of strings
    # each string in the list represents a page of the original document
    z = (clean.split('{BREAK}'))

    # removes extra whitespace at the beginning of each page
    for i in range(len(z)):
        formatted_page = re.sub("\s+", ' ', z[i])
        z[i] = formatted_page

    # adds each page to pages_dict with the page name as the key
    pages_dict = {}
    for i in range(len(z)):
        try:
            list_to_dict = (z[i].split('{TEXT}:'))
            pages_dict[list_to_dict[0]] = list_to_dict[1]
        except:
            print(z[i])

    # turns the dictionary into a list
    data = []
    page_names_list = []
    for i in pages_dict:
        page_names_list.append(i)
        data.append(pages_dict[i])

    # gets the final page of the manuscript, used to keep users from clicking to a page that doesn't exist when using the next button on the page
    final_page = page_names_list[-1]
    try:
        text = (pages_dict[page_name_input])
    except:
        return 'Page not found' #TODO IMPROVE THIS

    # tells user if the page is blank
    if text == ' ':
        text = 'Page intentionally left blank'

    

    # determines if the pages are labelled using 2 or 3 digits, ex: Page_01 or Page_001
    digits = final_page.split('_')[-1]
    num_page_digits = len(digits)

    page_number = page_name_input[(len(page_name_input) - num_page_digits) : len(page_name_input)].lstrip("0")
    final_number = final_page[(len(final_page) - num_page_digits) : len(final_page)].lstrip("0")

    return templates.TemplateResponse('page_new.html',{'request': request, 'text': text, 'title': title,
                                                                           'page_name': page_name_input,
                                                                           'final_page': final_page,
                                                                           'num_page_digits': num_page_digits,
                                                                           'page_number': page_number,
                                                                           'final_number': final_number,                                                                           
                                                                           'manuscript_name': manuscript_name})