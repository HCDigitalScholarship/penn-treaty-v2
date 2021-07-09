import csv
import os
from bs4 import BeautifulSoup
import re
import json


people_related = {}
places_related = {}
org_related = {}



for filename in os.listdir('tei_xml_files/swarthmore'):
    filename = 'swarthmore/' + filename
    source = 'tei_xml_files/' + filename
    soup = BeautifulSoup(open(source, encoding="utf8"), 'lxml')
    
    title = soup.find('title')
    title = title.string.split(':')[0]
    title = re.sub("\s+", ' ', title)

    for tag in soup.find_all():
        if tag.name == 'pb':
            page_number = tag.get('facs')
        if tag.name == 'persname':
            # gets the unique id for the person
            id = tag.get('key')
            people_related.setdefault(id, {}).setdefault(filename, {'title': title}).update({page_number: None})    
        elif tag.name == 'placename':
            # gets rid of checkPlace tags, which do not have a key in the xml
            if tag.string == 'checkPlace':
                tag.decompose()
            else:
                # gets the unique id for the place
                id = tag.get('key')
                try:
                    if id is not None:
                        places_related.setdefault(id, {}).setdefault(filename, {'title': title}).update({page_number: None})                 
                except:
                    print(tag)
        elif tag.name == 'orgname':
            # gets the unique id for the organization
            id = tag.get('key')
            try:
                # saves the contents of the tag temporarily, then replaces the tag contents with an html link element
                if id is not None:
                    org_related.setdefault(id, {}).setdefault(filename, {'title': title}).update({page_number: None})              
            except:
                print(tag)

for filename in os.listdir('tei_xml_files/haverford'):
    filename = 'haverford/' + filename
    source = 'tei_xml_files/' + filename
    soup = BeautifulSoup(open(source, encoding="utf8"), 'lxml')
    
    title = soup.find('title')
    title = title.string.split(':')[0]
    title = re.sub("\s+", ' ', title)

    for tag in soup.find_all():
        if tag.name == 'pb':
            page_number = tag.get('facs')
        if tag.name == 'persname':
            # gets the unique id for the person
            id = tag.get('key')
            people_related.setdefault(id, {}).setdefault(filename, {'title': title}).update({page_number: None})    
        elif tag.name == 'placename':
            # gets rid of checkPlace tags, which do not have a key in the xml
            if tag.string == 'checkPlace':
                tag.decompose()
            else:
                # gets the unique id for the place
                id = tag.get('key')
                try:
                    if id is not None:
                        places_related.setdefault(id, {}).setdefault(filename, {'title': title}).update({page_number: None})              
                except:
                    print(tag)
        elif tag.name == 'orgname':
            # gets the unique id for the organization
            id = tag.get('key')
            try:
                # saves the contents of the tag temporarily, then replaces the tag contents with an html link element
                if id is not None:
                    org_related.setdefault(id, {}).setdefault(filename, {'title': title}).update({page_number: None})             
            except:
                print(tag)

with open('people_related_pages.txt', 'w') as outfile:
    json.dump(people_related, outfile, indent=4)
    
with open('places_related_pages.txt', 'w') as outfile:
    json.dump(places_related, outfile, indent=4)
    
with open('org_related_pages.txt', 'w') as outfile:
    json.dump(org_related, outfile, indent=4)

