#!/usr/bin/env python

import gtk
import webkit
import string
import xml.etree.ElementTree as ET

global browser
global window

pages = dict()

def CloseWindow(caller_widget):
    #future settings here to either just close the GUI
    #or kill the app entirely
    gtk.main_quit() 
    
def title_changed(webview, frame, title):
    global window
    window.set_title(title)

def CreateMenuBar(agr):
    menuBar = gtk.MenuBar()
    
    fileMenu = gtk.Menu()
    itemFile = gtk.MenuItem("File")
    itemFile.set_submenu(fileMenu)    

    options = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES, agr)
    #somehow create an options panel here for some simple settings and adding
    #which sites you want to monitor
    fileMenu.append(options)

    #why no icon show up
    exit = gtk.ImageMenuItem(gtk.STOCK_CLOSE, agr)
    #exit = gtk.MenuItem("Exit")
    exit.connect("activate", gtk.main_quit)
    fileMenu.append(exit)
    
    menuBar.append(itemFile)
    return menuBar
    
def CreateButton(hbox, labeltext, imagepath):
    box = gtk.HBox(False, 0)
    
    image = gtk.Image()
    image.set_from_file(imagepath)
    
    label = gtk.Label(labeltext)  

    box.pack_start(image, False, False, 3)
    box.pack_start(label, False, False, 3)
    
    button = gtk.Button()
    button.add(box)
    button.connect("clicked", button_clicked)
    
    hbox.pack_start(button)
    
def CreateNavButton(hbox, icon):
    image = gtk.Image()
    image.set_from_stock(icon, 32)
    button = gtk.Button()
    button.add(image)
    hbox.pack_start(button)
     
def CreateButtonBar(win):
    hbox = gtk.HBox(False, 5)
    
    if pages.get('sabnzbd+'):
      CreateButton(hbox, "SABnzbd+", "img/sabnzbd.png")
    if pages.get('sick beard'):
      CreateButton(hbox, "Sick Beard", "img/sickbeard.png")
    if pages.get('couch potato'):
      CreateButton(hbox, "Couch Potato", "img/couchpotato.png")
    if pages.get('headphones'):
      CreateButton(hbox, "Headphones", "img/headphones.png")
    if pages.get('nzbmatrix'):
      CreateButton(hbox, "NZBMatrix", "img/nzbmatrix.png")
    if pages.get('dognzb'):
      CreateButton(hbox, "DogNZB", "img/dognzb.png")
    if pages.get('nzbs.org'):
      CreateButton(hbox, "NZBs.org","img/dognzb.png")
    
    CreateNavButton(hbox, gtk.STOCK_GO_BACK)
    CreateNavButton(hbox, gtk.STOCK_GO_FORWARD)
    CreateNavButton(hbox, gtk.STOCK_REFRESH)
    
    return hbox
    
def button_clicked(button):
    #ugly but works
    buttonName = button.get_child().get_children()[1].get_label()
    url = pages[string.lower(buttonName)][0]
    global browser
    browser.open(url)
    
def CreateWebBox():
    web = webkit.WebView()
    settings = web.get_settings()
    #what does this do?
    settings.set_property("enable-universal-access-from-file-uris", True)
    return web
    
      
window = gtk.Window()

window.set_position(gtk.WIN_POS_CENTER)
window.resize(600, 600)

window.connect("destroy", CloseWindow)

#open the config file tabs:
tree = ET.parse('config.xml')
root=tree.getroot()

for page in root.findall('page'):
  name = page.find('name').text
  url = page.find('url').text
  enabled = int(page.find('enabled').text)
  if enabled:
    pages[name] = [url,enabled]

agr = gtk.AccelGroup()
window.add_accel_group(agr)
menuBar = CreateMenuBar(agr)
hbox = CreateButtonBar(window)



browser = CreateWebBox()
browser.open(pages['sabnzbd+'][0])
browser.connect("title-changed", title_changed)

scroller = gtk.ScrolledWindow()
scroller.add(browser)

vbox = gtk.VBox(False, 2)
vbox.pack_start(menuBar, False, False, 0)
vbox.pack_start(hbox, False, False, 0)
vbox.pack_start(scroller)
window.add(vbox)
window.show_all()
gtk.main()
