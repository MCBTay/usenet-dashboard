#!/usr/bin/env python

import gtk
import webkit
import string

pages = dict()
global browser
global window

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

    options = gtk.MenuItem("Options")
    #somehow create an options panel here for some simple settings and adding
    #which sites you want to monitor
    fileMenu.append(options)

    #why no icon show up
    exit = gtk.ImageMenuItem(gtk.STOCK_QUIT, agr)
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
    return button
     
def CreateButtonBar(win):
    hbox = gtk.HBox(False, 5)
    
    sabnzbd = CreateButton(hbox, "SABnzbd+", "img/sabnzbd.png")
    sickbeard = CreateButton(hbox, "Sick Beard", "img/sickbeard.png")
    couchpotato = CreateButton(hbox, "Couch Potato", "img/couchpotato.png")
    headphones = CreateButton(hbox, "Headphones", "img/headphones.png")
    nzbmatrix = CreateButton(hbox, "NZBMatrix", "img/nzbmatrix.png")
    dognzb = CreateButton(hbox, "DogNZB", "img/sabnzbd.png")

    hbox.pack_start(sabnzbd)
    hbox.pack_start(sickbeard)
    hbox.pack_start(couchpotato)
    hbox.pack_start(headphones)
    hbox.pack_start(nzbmatrix)
    hbox.pack_start(dognzb)             
    
    return hbox
    
def button_clicked(button):
    #ugly but works
    buttonName = button.get_child().get_children()[1].get_label()
    url = pages[string.lower(buttonName)]
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
window.resize(500, 500)

window.connect("destroy", CloseWindow)


agr = gtk.AccelGroup()
window.add_accel_group(agr)
menuBar = CreateMenuBar(agr)
hbox = CreateButtonBar(window)

pages['sabnzbd+'] = 'http://localhost:8080/sabnzbd'
pages['sick beard'] = 'http://localhost:8081/home/'
pages['couch potato'] = 'http://localhost:5000/movie/'
pages['nzbmatrix'] = 'http://nzbmatrix.com/index.php'
pages['dognzb'] = 'https://dognzb.cr/browse';

browser = CreateWebBox()
browser.open(pages['sabnzbd+'])
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
