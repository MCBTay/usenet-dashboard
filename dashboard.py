#!/usr/bin/env python

import gtk
import webkit
import string
import xml.etree.ElementTree as ET
from preferences_window import PreferencesWindow

global menuBar, buttonBar, browser
global window
global configFile

pages = dict()

# Callbacks #
def close_window(caller_widget):
    #future settings here to either just close the GUI
    #or kill the app entirely
    gtk.main_quit() 
    
def create_preferences_window(caller_widget):
    PreferencesWindow()
    
    
def title_changed(webview, frame, title):
    global window
    window.set_title(title)
    
def button_clicked(button):
    #ugly but works
    buttonName = button.get_child().get_children()[1].get_label()
    url = pages[buttonName][1]
    global browser
    browser.open(url)
# End Callbacks #

def CreateMenuBar(agr):
    menuBar = gtk.MenuBar()
    
    fileMenu = gtk.Menu()
    itemFile = gtk.MenuItem("File")
    itemFile.set_submenu(fileMenu)    

    preferences = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES, agr)
    preferences.connect("activate", create_preferences_window)
    fileMenu.append(preferences)

    exit = gtk.ImageMenuItem(gtk.STOCK_CLOSE, agr)
    exit.connect("activate", gtk.main_quit)
    fileMenu.append(exit)
    
    menuBar.append(itemFile)
    return menuBar
    
def CreateButton(hbox, name):
    #vbox = gtk.VBox(False, 0)
    box = gtk.HBox(False, 0)
    
    image = gtk.Image()
    image.set_from_file(pages[name][2])
    
    label = gtk.Label(name)  

    box.pack_start(image, False)
    box.pack_start(label, False)
    
    button = gtk.Button()
    #vbox.pack_start(box)
    #vbox.pack_start(gtk.Label("Page title.......?"))
    button.add(box)
    button.connect("clicked", button_clicked)
    
    hbox.pack_start(button, False)
    
def CreateNavButton(hbox, icon):
    image = gtk.Image()
    image.set_from_stock(icon, 32)
    button = gtk.Button()
    button.add(image)
    hbox.pack_start(button, False)
     
def CreateButtonBar(win):
    global configFile, buttonBar 
    
    buttonBar = gtk.HBox(False, 5)
    
    if configFile:
        count = 1
        while count <= len(pages):
            for page in pages:
                if int(pages[page][0]) == count:
                    CreateButton(buttonBar, page)
            count = count + 1
    
    buttonBar.pack_start(gtk.Label(''), True, False)

    CreateNavButton(buttonBar, gtk.STOCK_GO_BACK)
    CreateNavButton(buttonBar, gtk.STOCK_GO_FORWARD)
    CreateNavButton(buttonBar, gtk.STOCK_REFRESH)
    
    return buttonBar

    
def CreateWebBox():
    web = webkit.WebView()
    settings = web.get_settings()
    settings.set_property('enable-page-cache', True)
    return web

def WriteConfig():
    global configFile
    
    root = ET.Element("")

def ParseConfig():
    global configFile, window
    try:
        configFile = open('./config.xml')
    except IOError:
       configFile = None

    if configFile:
        tree = ET.parse('config.xml')
        root = tree.getroot()
        for page in root.findall('page'):
          name = page.find('name').text
          url  = page.find('url').text
          img  = page.find('img').text
          order= page.find('order').text
          pages[name] = [order, url, img]
    else:
        PreferencesWindow()
        
def GetFirst(iterable, default=None):
    if iterable:
        for item in iterable:
            return item
    return default
        

      
window = gtk.Window()

window.set_position(gtk.WIN_POS_CENTER)
window.resize(1024, 768)

window.connect('destroy', close_window)

ParseConfig()

agr = gtk.AccelGroup()
window.add_accel_group(agr)
menuBar = CreateMenuBar(agr)
hbox = CreateButtonBar(window)

browser = CreateWebBox()

if configFile:
    # even uglier, still works -- need to clean dear god
    # had to do this to ensure you get the first one, in order of insertion
    # !!! This already bit me in the ass haha
    buttonName = buttonBar.get_children()[0].get_children()[0].get_children()[1].get_label()
    url = pages[buttonName][1]
    browser.open(url)
    
browser.connect('title-changed', title_changed)

scroller = gtk.ScrolledWindow()
scroller.add(browser)

vbox = gtk.VBox(False, 2)
vbox.pack_start(menuBar, False, False, 0)
vbox.pack_start(hbox, False, False, 0)
vbox.pack_start(scroller)
window.add(vbox)
window.show_all()
gtk.main()
