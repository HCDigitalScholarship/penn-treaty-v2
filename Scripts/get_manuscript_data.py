import os
from bs4 import BeautifulSoup
import re

sw_manuscript_list = []

for filename in os.listdir('../Text_Files/Swarthmore_Text_Files'):
    sw_manuscript_list.append(filename.split(':')[0])

sw_data = []

for filename in os.listdir('../tei_xml_files/swarthmore'):
    entry = []
    filename = 'swarthmore/' + filename
    source = '../tei_xml_files/' + filename
    soup = BeautifulSoup(open(source), 'lxml')

    # get first page using above code
    for tag in soup.find_all('pb'):
        page_name = tag.get('facs')
        if page_name:
            # page_url = ('/full_manuscript/' + filename + '/' + page_name)
            page_url = (filename + '/' + page_name)
        else:
            print("FAILED " + filename)
            page_url = None
        break

    for tag in soup.find('title'):
        title = tag.string.split(':')[0]
        # contents = re.sub('  +', '', contents)
        title = re.sub("\s+", ' ', title)

    for i in range(len(sw_manuscript_list)):
        if title == sw_manuscript_list[i]:
            # raw_text_url = '/sw_manuscript/' + str(i)
            raw_text_url = 'sw_manuscript/' + str(i)
    entry.append(title)
    entry.append(page_url)
    entry.append(raw_text_url)
    # print(entry)
    # print('\n')
    sw_data.append(entry)

print(sw_data)



hc_manuscript_list = []

for filename in os.listdir('../Text_Files/Haverford_Text_Files'):
    hc_manuscript_list.append(filename.split(':')[0])

hc_data = []

for filename in os.listdir('../tei_xml_files/haverford'):
    entry = []
    filename = 'haverford/' + filename
    source = '../tei_xml_files/' + filename
    soup = BeautifulSoup(open(source), 'lxml')

    # get first page using above code
    for tag in soup.find_all('pb'):
        page_name = tag.get('facs')
        if page_name:
            # page_url = ('/full_manuscript/' + filename + '/' + page_name)
            page_url = (filename + '/' + page_name)
        else:
            print("FAILED " + filename)
            page_url = None
        break

    for tag in soup.find('title'):
        title = tag.string.split(':')[0]
        # contents = re.sub('  +', '', contents)
        title = re.sub("\s+", ' ', title)

    for i in range(len(hc_manuscript_list)):
        if title == hc_manuscript_list[i]:
            # raw_text_url = '/hc_manuscript/' + str(i)
            raw_text_url = 'hc_manuscript/' + str(i)
    entry.append(title)
    entry.append(page_url)
    entry.append(raw_text_url)
    # print(entry)
    # print('\n')
    hc_data.append(entry)

print(hc_data)
