#!/usr/bin/env python

import gtk
import webkit
import string
import xml.etree.ElementTree as ET
from preferences_window import PreferencesWindow

global menuBar, buttonBar, browser, progress
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
    
def back_button_clicked(button):
    global browser
    browser.go_back()
def forward_button_clicked(button):
    global browser
    browser.go_forward()
def refresh_button_clicked(button):
    global browser
    browser.reload()
    
def load_progress_changed(webview, amount):
    global progress
    progress.set_fraction(amount / 100.0)
    
def load_started(webview, frame):
    global progress
    progress.set_visible(True)
    
def load_finished(webview, frame):
    global progress
    progress.set_visible(False)
# End Callbacks #

def CreateMenuBar(agr):
    menuBar = gtk.MenuBar()
    
    fileMenu = gtk.Menu()
    itemFile = gtk.MenuItem('File')
    itemFile.set_submenu(fileMenu)    

    preferences = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES, agr)
    preferences.connect('activate', create_preferences_window)
    fileMenu.append(preferences)

    exit = gtk.ImageMenuItem(gtk.STOCK_CLOSE, agr)
    exit.connect('activate', gtk.main_quit)
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
    button.connect('clicked', button_clicked)
    
    hbox.pack_start(button, False)
    
def CreateNavButton(hbox, icon):
    image = gtk.Image()
    image.set_from_stock(icon, 32)
    button = gtk.Button()
    button.add(image)
    hbox.pack_start(button, False)
    return button
     
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

    back    = CreateNavButton(buttonBar, gtk.STOCK_GO_BACK)
    back.connect('clicked', back_button_clicked)
    forward = CreateNavButton(buttonBar, gtk.STOCK_GO_FORWARD)
    forward.connect('clicked', forward_button_clicked)
    refresh = CreateNavButton(buttonBar, gtk.STOCK_REFRESH)
    refresh.connect('clicked', refresh_button_clicked)    
    return buttonBar

    
def CreateWebBox():
    web = webkit.WebView()
    settings = web.get_settings()
    settings.set_property('enable-page-cache', True)
    return web

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
browser.connect('load-started', load_started)
browser.connect('load-progress-changed', load_progress_changed)
browser.connect('load-finished', load_finished)

scroller = gtk.ScrolledWindow()
scroller.add(browser)

progress = gtk.ProgressBar()

vbox = gtk.VBox(False, 2)
vbox.pack_start(menuBar, False, False, 0)
vbox.pack_start(hbox, False, False, 0)
vbox.pack_start(scroller)
vbox.pack_start(progress, False)
window.add(vbox)
window.show_all()
gtk.main()
