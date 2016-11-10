import xml.etree.ElementTree as ET
tree = ET.parse('project1.lpi')
root = tree.getroot()

print root.tag, root.attrib
print '/'*55
for child in root:
    print child.tag, child.attrib
print '*'*55
for c in root.find('ProjectOptions'):
    print c.tag, c.attrib
print '>'*55
print """<?xml version="1.0" encoding="UTF-8"?>"""
print ET.tostring( root )
#ET.dump( root )
print '-'*55
for node in tree.iter():
    print node.tag, node.attrib
    
    if node.text:
        s = str(node.text).strip()
        if s:
            print '    --TEXT-->"%s"'%s  
    if node.tail:            
        s = str(node.tail).strip()
        if s:
            print '    --TAIL-->"%s"'%s