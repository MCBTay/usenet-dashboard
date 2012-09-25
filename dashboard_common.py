import os
import xml.etree.ElementTree as ET
import preferences_window

config_filepath = os.path.join(os.path.dirname(__file__), 'config.xml')

def ParseConfig(trigger_preferences=False):
    pages = dict()
    
    try:
        config_file = open(config_filepath)
    except IOError:
        config_file = None

    if config_file:
        tree = ET.parse(config_filepath)
        root = tree.getroot()
        for page in root.findall('page'):
            name = page.find('name').text
            url = page.find('url').text
            img = page.find('img').text
            order = page.find('order').text
            pages[name] = [order, url, img]
        return pages
    else:
        if trigger_preferences:
            preferences_window.PreferencesWindow()
            
def WriteConfig(pages):
    open(config_filepath, 'w+')
        
    root = ET.Element('pages')
    for name in pages:
        order = pages[name][0]
        url   = pages[name][1]
        img   = pages[name][2]

        pageNode = ET.SubElement(root, 'page')
        
        orderNode = ET.SubElement(pageNode, 'order')
        orderNode.text = order
        
        nameNode = ET.SubElement(pageNode, 'name')
        nameNode.text = name
        
        urlNode = ET.SubElement(pageNode, 'url')
        urlNode.text = url
        
        imgNode = ET.SubElement(pageNode, 'img')                        
        imgNode.text = img
    
    tree = ET.ElementTree(root)
    PrettyPrint(root)
    tree.write(config_filepath)
    
def PrettyPrint(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            PrettyPrint(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i      
