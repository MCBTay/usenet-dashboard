#!/usr/bin/env python

import gtk
import webkit
import string

pages = dict()
global browser

def CloseWindow(caller_widget):
    #future settings here to either just close the GUI
    #or kill the app entirely
    gtk.main_quit() 

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
    menuBar.show()
    return menuBar
    
def CreateButton(hbox, labeltext, imagepath):
    box = gtk.HBox(False, 0)
    
    image = gtk.Image()
    image.set_from_file(imagepath)
    image.show()
    label = gtk.Label(labeltext)
    label.show()    

    box.pack_start(image, False, False, 3)
    box.pack_start(label, False, False, 3)
    
    button = gtk.Button()
    button.add(box)
    return button
     
def CreateButtonBar(win):
    hbox = gtk.HBox(False, 5)
    hbox.show()
    
    sabnzbd = CreateButton(hbox, "SABnzbd+", "img/sabnzbd.png")
    sabnzbd.connect("clicked", button_clicked)
    sickbeard = CreateButton(hbox, "Sick Beard", "img/sickbeard.png")
    sickbeard.connect("clicked", button_clicked)
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
    
    
win = gtk.Window()

win.set_title("Usenet Dashboard")
win.set_position(gtk.WIN_POS_CENTER)

win.connect("destroy", CloseWindow)

agr = gtk.AccelGroup()
win.add_accel_group(agr)
menuBar = CreateMenuBar(agr)
hbox = CreateButtonBar(win)

pages['sabnzbd+'] = 'http://localhost:8080/sabnzbd'
pages['sick beard'] = 'http://localhost:8081/home/'

browser = CreateWebBox()
browser.open(pages['sabnzbd+'])
browser.show()

vbox = gtk.VBox(False, 2)
vbox.pack_start(menuBar, False, False, 0)
vbox.pack_start(hbox, False, False, 0)
vbox.pack_start(browser, False, False, 0)
win.add(vbox)
win.show_all()
gtk.main()
