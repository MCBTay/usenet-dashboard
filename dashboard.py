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

class Dashboard:
    pages = dict()

    # Callbacks #
    def close_window(self, caller_widget):
        gtk.main_quit() 
        
    def create_preferences_window(self, caller_widget):
        PreferencesWindow()
        
    def button_clicked(self, button):
        #ugly but works
        buttonName = button.get_child().get_children()[1].get_label()
        url = self.pages[buttonName][1]
        self.browser.open(url)
        
    def back_button_clicked(self, button):
        self.browser.go_back()

    def forward_button_clicked(self, button):
        self.browser.go_forward()
        
    def refresh_button_clicked(self, button):
        self.browser.reload()
        
    def download_requested(self, webview, download):
        print 'trying to download', download
        download.set_destination_uri('.')
        download.start()
        return True
        
    def load_progress_changed(self, webview, amount):
        self.progress.set_fraction(amount / 100.0)
        
    def load_started(self, webview, frame):
        self.progress.set_visible(True)
        
    def load_finished(self, webview, frame):
        self.progress.set_visible(False)
        
    def create_about_window(self, caller_widget):
        AboutWindow()

    def on_key_press(self, caller_widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname == 'F5':
            self.browser.reload()
    # End Callbacks #
        
    def CreateButton(self, hbox, name):
        box = gtk.HBox(False, 0)
        
        image = gtk.Image()
        image.set_from_file(self.pages[name][2])
        
        label = gtk.Label(name)  

        box.pack_start(image, False)
        box.pack_start(label, False)
        
        button = gtk.Button()
        button.add(box)
        button.connect('clicked', self.button_clicked)
        
        hbox.pack_start(button, False)
        
    def CreateNavButton(self, hbox, icon):
        image = gtk.Image()
        image.set_from_stock(icon, 3)
        button = gtk.Button()
        button.add(image)
        hbox.pack_start(button, False)
        return button
         
    def CreateButtonBar(self, win):
        
        self.button_bar = gtk.HBox(False, 5)
        
        if self.pages:
            sorted_pages = sorted(self.pages.iteritems(), key=operator.itemgetter(1))
            for page in sorted_pages:
                self.CreateButton(self.button_bar, page[0])
        
        self.button_bar.pack_start(gtk.Label(''), True, False)
        
        about = self.CreateNavButton(self.button_bar, gtk.STOCK_ABOUT)
        about.connect('clicked', self.create_about_window)
        
        settings = self.CreateNavButton(self.button_bar, gtk.STOCK_PREFERENCES)
        settings.connect('clicked', self.create_preferences_window)

        back    = self.CreateNavButton(self.button_bar, gtk.STOCK_GO_BACK)
        back.connect('clicked', self.back_button_clicked)
        forward = self.CreateNavButton(self.button_bar, gtk.STOCK_GO_FORWARD)
        forward.connect('clicked', self.forward_button_clicked)
        refresh = self.CreateNavButton(self.button_bar, gtk.STOCK_REFRESH)
        refresh.connect('clicked', self.refresh_button_clicked)    
        return self.button_bar
     
    def CreateWebBox(self):
        web = webkit.WebView()
        settings = web.get_settings()
        settings.set_property('enable-page-cache', True)
        return web
    
    def __init__(self):
        window = gtk.Window()
        iconFilepath = os.path.join(os.path.dirname(__file__), 'img/icon.svg')
        window.set_icon_from_file(iconFilepath);
        window.set_position(gtk.WIN_POS_CENTER)
        window.resize(1024, 768)
        window.set_title('Usenet Dashboard')
        window.connect('destroy', self.close_window)
        window.connect('key_press_event', self.on_key_press)

        self.pages = dashboard_common.ParseConfig(True)
        agr = gtk.AccelGroup()
        window.add_accel_group(agr)
        hbox = self.CreateButtonBar(window)

        self.browser = self.CreateWebBox()

        if self.pages:
            # even uglier, still works -- need to clean dear god
            # had to do this to ensure you get the first one, in order of insertion
            # !!! This already bit me in the ass haha -- and again
            print self.button_bar.get_children()
            buttonName = self.button_bar.get_children()[0].get_children()[0].get_children()[1].get_label()
            url = self.pages[buttonName][1]
            self.browser.open(url)
            
        self.browser.connect('load-started', self.load_started)
        self.browser.connect('load-progress-changed', self.load_progress_changed)
        self.browser.connect('load-finished', self.load_finished)
        self.browser.connect('download-requested', self.download_requested)

        scroller = gtk.ScrolledWindow()
        scroller.add(self.browser)

        self.progress = gtk.ProgressBar()

        vbox = gtk.VBox(False, 2)
        vbox.pack_start(hbox, False, False, 0)
        vbox.pack_start(scroller)
        vbox.pack_start(self.progress, False)
        window.add(vbox)
        window.show_all()        


Dashboard()
gtk.main()
