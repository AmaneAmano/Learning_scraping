from xml.dom import minidom

d = minidom.Document()
link = d.createCDATASection('<a href="http://example.com">This is an example of link markup.</a>')
print(link.toxml())
print(link)