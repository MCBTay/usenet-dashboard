import os
import xml.etree.ElementTree as ET
import preferences_window

config_filepath = os.path.join(os.path.dirname(__file__), 'config.xml')

def ParseConfig(trigger_preferences=False):
    try:
        config_file = open(config_filepath)
    except IOError:
        config_file = None

    if config_file:
        configuration = dict()
        tree = ET.parse(config_filepath)
        root = tree.getroot()
        for child in root:
            if child.tag == 'settings':
                settings = dict()
                for setting in child:
                    settings[setting.tag] = setting.text
                configuration['settings'] = settings
            if child.tag == 'pages':
                pages = dict()
                for page in child.findall('page'):
                    name = page.find('name').text
                    url = page.find('url').text
                    img = page.find('img').text
                    order = page.find('order').text
                    pages[name] = [order, url, img]
                configuration['pages'] = pages
        return configuration            
    else:
        if trigger_preferences:
            preferences_window.PreferencesWindow()
            
def WriteConfig(configuration):
    open(config_filepath, 'w+')
    
    root = ET.Element('configuration')
    
    for child in configuration:
        child_node = ET.SubElement(root, child)
        if child == 'settings':
            for setting in configuration[child]:
                node = ET.SubElement(child_node, setting)
                node.text = configuration[child][setting]
        
        if child == 'pages':   
            for name in configuration[child]:
                order = configuration[child][name][0]
                url   = configuration[child][name][1]
                img   = configuration[child][name][2]

                page_node = ET.SubElement(child_node, 'page')
                
                order_node = ET.SubElement(page_node, 'order')
                order_node.text = order
                
                name_node = ET.SubElement(page_node, 'name')
                name_node.text = name
                
                url_node = ET.SubElement(page_node, 'url')
                url_node.text = url
                
                img_node = ET.SubElement(page_node, 'img')                        
                img_node.text = img
    
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
