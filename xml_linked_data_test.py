from bs4 import BeautifulSoup
import os




# for persName in soup.find_all('persname'):
#     key = persName.get('key')
#     old_contents = persName.contents
#     s = (old_contents[0])
#     url = 'http://127.0.0.1:8000/people/' + key
#     a = soup.new_tag("a", href=url)
#     a.string = s
#     persName.wrap(a)
#     persName.string = ''


# TODO FIXED "checkPlace" error
def create_linked_xml(source):
    infile = open(source, "r")
    contents = infile.read()

    soup = BeautifulSoup(contents, 'lxml')

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
            elif tag.name == 'lb':
                br = soup.new_tag('br')
                tag.replace_with(br)
        except:
            print('error at:')
            print(tag)

    title = 'linked_' + source.split('/')[2].split('.')[0] + '.html'
    print(title)

    directory = '''/Users/simon/PycharmProjects/DigitalScholarship/Penn's Treaty/penn-treaty-v2/templates/Linked HTML Files/Swarthmore/''' + title


    with open(directory, "w") as file:
        file.write(str(soup))


#create_linked_xml('tei_xml_files/swarthmore/SW_SH1799.xml')

for filename in os.listdir('tei_xml_files/swarthmore'):
    path = 'tei_xml_files/swarthmore/' + filename
    create_linked_xml(path)



