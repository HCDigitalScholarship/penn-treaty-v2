from bs4 import BeautifulSoup
import re

soup = BeautifulSoup(open('../Random/SW_JC1797_TEST.xml'), 'lxml')
#soup = BeautifulSoup(open('../Random/linked_hv_allinsonw_diary_1809_v1.xml'), 'lxml')


for tag in soup.find_all():
    if tag.name == 'persname':
        tag.unwrap()
    elif tag.name == 'placename':
        if tag.string == 'checkPlace':
            tag.decompose()
        else:
            tag.unwrap()
    elif tag.name =='orgName':
        tag.unwrap()
        # if id != None:
        #     tag.contents.append('{' + id + '}')
        # TODO add id's for links


s = ''

# add breaks
for tag in soup.find_all('pb'):
    page_name = tag.get('facs')
    print(page_name)
    tag.string = '{BREAK}'+page_name+'{TEXT}:'

document = soup.find('text')


pages_list = (str(document)).split('{BREAK}')

x = str(document)

x = x.replace('<lb></lb>','\n')
x = x.replace('&amp','&')


clean = re.sub('<[^>]+>', '', x)

z = (clean.split('{BREAK}'))

for i in range(len(z)):
    formatted_page = re.sub("\s+", ' ',z[i])
    z[i] = formatted_page

pages_dict = {}
for i in range(len(z)):
    try:
        list_to_dict = (z[i].split('{TEXT}:'))
        pages_dict[list_to_dict[0]] = list_to_dict[1]
    except:
        print(z[i])

print(pages_dict)





# for page in z:
#     print(page)
#     print('\n')
