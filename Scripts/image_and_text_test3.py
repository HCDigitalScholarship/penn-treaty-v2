from bs4 import BeautifulSoup
import re

soup = BeautifulSoup(open('../Random/SW_JC1797_TEST.xml'), 'lxml')
#soup = BeautifulSoup(open('../Random/linked_hv_allinsonw_diary_1809_v1.xml'), 'lxml')

#soup = BeautifulSoup(open('''/Users/simon/PycharmProjects/DigitalScholarship/Penn's Treaty/penn-treaty-v2/templates/Linked XML Files/Swarthmore/linked_SW_JC1797.xml'''), 'lxml')

#soup = BeautifulSoup(open('''/Users/simon/PycharmProjects/DigitalScholarship/Penn's Treaty/penn-treaty-v2/tei_xml_files/swarthmore/SW_JC1797.xml'''), 'lxml')

# TODO get rid of line breaks?
for tag in soup.find_all('lb'):
    tag.decompose()


for tag in soup.find_all():
    if tag.name == 'persname':
        print(tag.get('key'))
        id = tag.get('key')
        try:
            if id is not None:
                # tag.contents.append("ID: " + id)
                temp_tag_contents = tag.string
                if temp_tag_contents == None:
                    print("NONE TAG")
                    print(tag)
                    print(tag.contents)
                    tag.string = tag.contents.join('')
                tag.string = f'<a href="http://127.0.0.1:8000/people/{id}>{temp_tag_contents}</a>'
            tag.unwrap()
        except:
            print(tag)
    elif tag.name == 'placename':
        print(tag.get('key'))
        if tag.string == 'checkPlace':
            tag.decompose()
        else:
            print(tag.get('key'))
            id = tag.get('key')
            try:
                if id is not None:
                    # tag.contents.append("ID: " + id)
                    temp_tag_contents = tag.string
                    if temp_tag_contents == None:
                        print("NONE TAG")
                        print(tag)
                        print(tag.contents)
                        tag.string = tag.contents.join('')
                    tag.string = f'<a href="http://127.0.0.1:8000/places/{id}>{temp_tag_contents}</a>'
                tag.unwrap()
            except:
                print(tag)
    elif tag.name =='orgName':
        print(tag.get('key'))
        id = tag.get('key')
        try:
            if id is not None:
                # tag.contents.append("ID: " + id)
                temp_tag_contents = tag.string
                if temp_tag_contents == None:
                    print("NONE TAG")
                    print(tag)
                    print(tag.contents)
                    tag.string = tag.contents.join('')
                tag.string = f'<a href="http://127.0.0.1:8000/organizations/{id}>{temp_tag_contents}</a>'
            tag.unwrap()
        except:
            print(tag)
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

clean = clean.replace('&lt;','<')
clean = clean.replace('&gt;','>')

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

for key in pages_dict:
    print(pages_dict[key])



# for page in z:
#     print(page)
#     print('\n')
