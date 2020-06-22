from bs4 import BeautifulSoup
source = 'tei_xml_files/swarthmore/SW_JC1796.xml'
infile = open(source,"r")
contents = infile.read()

soup = BeautifulSoup(contents,'lxml')



# for persName in soup.find_all('persname'):
#     key = persName.get('key')
#     old_contents = persName.contents
#     s = (old_contents[0])
#     url = 'http://127.0.0.1:8000/people/' + key
#     a = soup.new_tag("a", href=url)
#     a.string = s
#     persName.wrap(a)
#     persName.string = ''





for tag in soup.find_all():
    try:
    # people
        if tag.name == 'persname':
            key = tag.get('key')
            old_contents = tag.contents
            # s = ''.join(str(elem) for elem in old_contents if str(elem) != '<lb></lb>')
            if len(old_contents) > 1:
                s = old_contents[0] + old_contents[2]
            else:
                s = old_contents[0]
            url = 'http://127.0.0.1:8000/people/' + key
            a = soup.new_tag("a", href=url)
            a.string = s
            tag.wrap(a)
            tag.string = ''
        elif tag.name == 'placename':
            key = tag.get('key')
            old_contents = tag.contents
            if len(old_contents) > 1:
                s = old_contents[0] + old_contents[2]
            else:
                s = old_contents[0]
            url = 'http://127.0.0.1:8000/places/' + key
            a = soup.new_tag("a", href=url)
            a.string = s
            tag.wrap(a)
            tag.string = ''
        elif tag.name == 'orgname':
            key = tag.get('key')
            old_contents = tag.contents
            if len(old_contents) > 1:
                s = old_contents[0] + old_contents[2]
            else:
                s = old_contents[0]
            url = 'http://127.0.0.1:8000/organizations/' + key
            a = soup.new_tag("a", href=url)
            a.string = s
            tag.wrap(a)
            tag.string = ''
    except:
        print('error at:')
        print(tag)



#
# print(soup)

with open("output1.html", "w") as file:
    file.write(str(soup))

