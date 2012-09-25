#!/usr/bin/env python

import os, sys, inspect
import gtk
import webkit
import string
import operator
import xml.etree.ElementTree as ET
from preferences_window import PreferencesWindow
from about_window import AboutWindow
import dashboard_common

global menuBar, buttonBar, browser, progress
global window

pages = dict()

# Callbacks #
def close_window(caller_widget):
    gtk.main_quit() 
    
def create_preferences_window(caller_widget):
    PreferencesWindow()
    
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
    
def download_requested(webview, download):
    print 'trying to download', download
    download.set_destination_uri('.')
    download.start()
    return True
    
def load_progress_changed(webview, amount):
    global progress
    progress.set_fraction(amount / 100.0)
    
def load_started(webview, frame):
    global progress
    progress.set_visible(True)
    
def load_finished(webview, frame):
    global progress
    progress.set_visible(False)
    
def create_about_window(caller_widget):
    AboutWindow()

def on_key_press(caller_widget, event):
    global browser
    keyname = gtk.gdk.keyval_name(event.keyval)
    if keyname == 'F5':
        browser.reload()

# End Callbacks #
    
def CreateButton(hbox, name):
    box = gtk.HBox(False, 0)
    
    image = gtk.Image()
    image.set_from_file(pages[name][2])
    
    label = gtk.Label(name)  

    box.pack_start(image, False)
    box.pack_start(label, False)
    
    button = gtk.Button()
    button.add(box)
    button.connect('clicked', button_clicked)
    
    hbox.pack_start(button, False)
    
def CreateNavButton(hbox, icon):
    image = gtk.Image()
    image.set_from_stock(icon, 3)
    button = gtk.Button()
    button.add(image)
    hbox.pack_start(button, False)
    return button
     
def CreateButtonBar(win):
    global buttonBar 
    
    buttonBar = gtk.HBox(False, 5)
    
    if pages:
        sorted_pages = sorted(pages.iteritems(), key=operator.itemgetter(1))
        for page in sorted_pages:
            CreateButton(buttonBar, page[0])
    
    buttonBar.pack_start(gtk.Label(''), True, False)
    
    about = CreateNavButton(buttonBar, gtk.STOCK_ABOUT)
    about.connect('clicked', create_about_window)
    
    settings = CreateNavButton(buttonBar, gtk.STOCK_PREFERENCES)
    settings.connect('clicked', create_preferences_window)

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
        
def GetFirst(iterable, default=None):
    if iterable:
        for item in iterable:
            return item
    return default
        
            
window = gtk.Window()
iconFilepath = os.path.join(os.path.dirname(__file__), 'img/icon.svg')
window.set_icon_from_file(iconFilepath);
window.set_position(gtk.WIN_POS_CENTER)
window.resize(1024, 768)
window.set_title('Usenet Dashboard')
window.connect('destroy', close_window)
window.connect('key_press_event', on_key_press)

pages = dashboard_common.ParseConfig(True)
agr = gtk.AccelGroup()
window.add_accel_group(agr)
hbox = CreateButtonBar(window)

browser = CreateWebBox()

if pages:
    # even uglier, still works -- need to clean dear god
    # had to do this to ensure you get the first one, in order of insertion
    # !!! This already bit me in the ass haha
    buttonName = buttonBar.get_children()[0].get_children()[0].get_children()[1].get_label()
    url = pages[buttonName][1]
    browser.open(url)
    
browser.connect('load-started', load_started)
browser.connect('load-progress-changed', load_progress_changed)
browser.connect('load-finished', load_finished)
browser.connect('download-requested', download_requested)

scroller = gtk.ScrolledWindow()
scroller.add(browser)

progress = gtk.ProgressBar()

vbox = gtk.VBox(False, 2)
vbox.pack_start(hbox, False, False, 0)
vbox.pack_start(scroller)
vbox.pack_start(progress, False)
window.add(vbox)
window.show_all()
gtk.main()
