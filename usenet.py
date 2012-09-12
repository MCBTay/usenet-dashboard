#!/usr/bin/env python

import gtk
import webkit

def CloseWindow(caller_widget):
    gtk.main_quit() 

def CreateMenuBar(agr):
    menuBar = gtk.MenuBar()
    
    fileMenu = gtk.Menu()
    itemFile = gtk.MenuItem("File")
    itemFile.set_submenu(fileMenu)    

    options = gtk.MenuItem("Options")
    #options.connect("activate", gtk.main_quit)
    #somehow create an options panel here for some simple settings and adding
    #which sites you want to monitor
    fileMenu.append(options)

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
    #win.add(hbox)
    
    sabnzbd = CreateButton(hbox, "SABnzbd+", "img/sabnzbd.png")
    sickbeard = CreateButton(hbox, "Sick Beard", "img/sickbeard.png")
    couchpotato = CreateButton(hbox, "Couch Potato", "img/couchpotato.png")
    headphones = CreateButton(hbox, "Headphones", "img/headphones.png")
    nzbmatrix = CreateButton(hbox, "NZBMatrix", "img/nzbmatrix.png")
    dognzb = CreateButton(hbox, "DogNZB", "img/sabnzbd.png")

    hbox.pack_start(sabnzbd)
    hbox.pack_start(sickbeard);
    hbox.pack_start(couchpotato);
    hbox.pack_start(headphones);
    hbox.pack_start(nzbmatrix);
    hbox.pack_start(dognzb);                
    
    return hbox
    
    
    
win = gtk.Window()

win.set_title("Simple Web Browser")
win.set_position(gtk.WIN_POS_CENTER)

win.connect("destroy", CloseWindow)

agr = gtk.AccelGroup()
win.add_accel_group(agr)
menuBar = CreateMenuBar(agr)
hbox = CreateButtonBar(win)

web = webkit.WebView()       
settings = web.get_settings()
settings.set_property("enable-universal-access-from-file-uris", True)
web.open("http://localhost:8080/sabnzbd/")
web.show()
#win.add(web)
vbox = gtk.VBox(False, 2)
vbox.pack_start(menuBar, False, False, 0)
vbox.pack_start(hbox, False, False, 0)
vbox.pack_start(web, False, False, 0)
win.add(vbox)
win.show_all()
gtk.main() # Enter the 'GTK mainloop', so that the GTK app starts to run
