from lxml import etree

# f=open('linked_SW_SH1799.xml')
# xml=f.read()
#
# root = etree.fromstring(xml)


root = etree.parse(r'linked_hv_allinsonw_diary_1809_v3.xml')
# Print the loaded XML
print(etree.tostring(root))


